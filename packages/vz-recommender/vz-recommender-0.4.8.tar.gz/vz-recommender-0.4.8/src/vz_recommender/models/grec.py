import abc
from typing import *

import torch
from torch import nn, Tensor
from transformers import AutoModel, DistilBertConfig, DistilBertModel

from .context import ContextHead, ContextTransformerAndWide
from .moe import MOELayer, Top2Gate, ExpertLayer, MoEFFLayer, MoEFFLayerTopK
from .mmoe import MMoE
from .transformer import (ParallelTransformerAEP, ParallelTransformerBlock, TransformerAEP, ParallelTransformerAEP2S,
                          TransformerHistory)
from .utils import MeanMaxPooling, LayerNorm, AutomaticWeightedLoss


#==========================================================================================================================
# Main Matching Model
#==========================================================================================================================
class GRecMatching(nn.Module):
        
    
    def __init__(
        self, 

        
        # Call
        call_num_wide,                    # num of wide features for the call
        call_deep_num_embedings_list,     # list if the number of embeddings (number of distinct values) for each deep call feature, e.g. 7 for days_of_week and 23 for time_of_day
        call_deep_embedding_dim_list,     # list of dimensionalities of each deep embedding
        
                
        # Customer
        customer_num_wide,                    # num of wide features for the customer
        customer_deep_num_embedings_list,     # list if the number of embeddings for each deep customer feature
        customer_deep_embedding_dim_list,     # list of dimensionalities of each deep embedding
        
        
        # Agent
        agent_num_wide,                    # num of wide features for the agent
        agent_deep_num_embedings_list,     # list if the number of embeddings for each deep call feature
        agent_deep_embedding_dim_list,     # list of dimensionalities of each deep embedding
        
        
        # Other params
        call_customer_agent_embedding_dim,  # Customer/Agent embeddings dimensionality that model will generate as part of output
        default_deep_embedding_dim
    ):
        
        
        super().__init__()
        
        
        # Store the dimensionality of the customer/agent embeddings to be generated
        self.call_customer_agent_embedding_dim = call_customer_agent_embedding_dim
        
        #-----------------------
        # Call 
        #-----------------------
        
        # Call: Wide
        self.call_num_wide        = call_num_wide
        self.call_wide_batch_norm = nn.BatchNorm1d(call_num_wide)
        
        # Call: Deep
        self.call_deep_embedding  = nn.ModuleList([
                nn.Embedding(num_embeddings, embedding_dim)
                for num_embeddings, embedding_dim in zip(call_deep_num_embedings_list, call_deep_embedding_dim_list)
            ])
        self.sum_call_embedding_dims = sum(call_deep_embedding_dim_list)

        
        #-----------------------
        # Customer 
        #-----------------------
        
        # Customer: Wide
        self.customer_num_wide        = customer_num_wide
        self.customer_wide_batch_norm = nn.BatchNorm1d(customer_num_wide)
        
        # Customer: Deep
        self.customer_deep_embedding  = nn.ModuleList([
                nn.Embedding(num_embeddings, embedding_dim)
                for num_embeddings, embedding_dim in zip(customer_deep_num_embedings_list, customer_deep_embedding_dim_list)
            ])
        self.sum_customer_embedding_dims = sum(customer_deep_embedding_dim_list)
        
        
        #-----------------------
        # Agent 
        #-----------------------
        
        # Agent: Wide
        self.agent_num_wide        = agent_num_wide
        self.agent_wide_batch_norm = nn.BatchNorm1d(agent_num_wide)
        
        # Agent: Deep
        self.agent_deep_embedding  = nn.ModuleList([
                nn.Embedding(num_embeddings, embedding_dim)
                for num_embeddings, embedding_dim in zip(agent_deep_num_embedings_list, agent_deep_embedding_dim_list)
            ])
        self.sum_agent_embedding_dims = sum(agent_deep_embedding_dim_list)

        
        
        
        
        
        #-------------------------------------
        # Tower 1:  Call-customer tower (Dynamic)
        #-------------------------------------
        call_customer_total_deep_dims = self.sum_call_embedding_dims + self.sum_customer_embedding_dims
        call_customer_total_wide_dims = self.call_num_wide           + self.customer_num_wide
        call_customer_all_dims        = call_customer_total_deep_dims + call_customer_total_wide_dims
        
        self.call_customer_dense1   = torch.nn.Linear(in_features=call_customer_all_dims, out_features=call_customer_all_dims // 2) 
        self.call_customer_act1     = nn.LeakyReLU(0.2)
        self.call_customer_dropout1 = nn.Dropout(p=0.1)   
        
        self.call_customer_dense2   = torch.nn.Linear(in_features=call_customer_all_dims // 2, out_features=call_customer_all_dims // 2) 
        self.call_customer_act2     = nn.LeakyReLU(0.2)
        self.call_customer_dropout2 = nn.Dropout(p=0.1) 
        
        
        self.call_customer_dense3   = torch.nn.Linear(in_features=call_customer_all_dims // 2, out_features=call_customer_agent_embedding_dim) 
        self.call_customer_act3     = nn.LeakyReLU(0.2)
        self.call_customer_dropout3 = nn.Dropout(p=0.1) 

        
        
        #-------------------------------------
        # Tower 2:  Agent tower (Static)
        #-------------------------------------
        agent_all_dims  = self.sum_agent_embedding_dims + self.agent_num_wide
        
        self.agent_dense1   = torch.nn.Linear(in_features=agent_all_dims, out_features=agent_all_dims // 2) 
        self.agent_act1     = nn.LeakyReLU(0.2)
        self.agent_dropout1 = nn.Dropout(p=0.1)   
        
        self.agent_dense2   = torch.nn.Linear(in_features=agent_all_dims // 2, out_features=agent_all_dims // 2) 
        self.agent_act2     = nn.LeakyReLU(0.2)
        self.agent_dropout2 = nn.Dropout(p=0.1) 
        
        
        self.agent_dense3   = torch.nn.Linear(in_features=agent_all_dims // 2, out_features=call_customer_agent_embedding_dim) 
        self.agent_act3     = nn.LeakyReLU(0.2)
        self.agent_dropout3 = nn.Dropout(p=0.1) 

        
        
        #-------------------------------------
        # Activation
        #------------------------------------- 
        self.final_activation = torch.nn.Sigmoid()
        
   

        
    
    
    # Dmitri: modified __getitem__(self, idx) to include next_item_in
    def forward(
        self,
        
        # Call
        call_deep_in: List[Tensor], 
        call_wide_in: List[Tensor],
        
        # Customer
        customer_deep_in: List[Tensor], 
        customer_wide_in: List[Tensor],
        
        # Agent
        agent_deep_in: List[Tensor], 
        agent_wide_in: List[Tensor]

        
    ):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        
        
        """
        Input is deep, wide & shared embedding
        
        Args:
            deep_in: list
            wide_in: list
            shared_in: list (default=None).

        Return:
            ctx_out: Tensor
        
        Shape:
            deep_in: [batch_size, deep_dims]
            wide_in: [batch_size, num_wide]
            shared_in: [batch_size, num_shared]
            ctx_out: [batch_size, len(deep_dims)*deep_embed_dims+(num_shared*seq_embed_dim)+num_wide]
        """
        
        
        #-------------------
        # Call
        #-------------------
        
        # Call: Deep
        call_deep_embedding_list = [self.call_deep_embedding[i](input_deep).unsqueeze(1)
                               for i, input_deep in enumerate(call_deep_in)]
        
        call_deep_out = torch.cat(call_deep_embedding_list, dim=2).squeeze(1)
        
        
        # Call: Wide
        call_wide_in_list = [wide_i.float() for wide_i in call_wide_in]
        call_wide_cat = torch.stack(call_wide_in_list, dim=0)
        call_wide_out = torch.transpose(call_wide_cat, dim1=1, dim0=0)
        
        
        # Call: Normalize
        call_wide_out = self.call_wide_batch_norm(call_wide_out)


        
        #-------------------
        # Customer
        #-------------------
        
        # Customer: Deep
        customer_deep_embedding_list = [self.customer_deep_embedding[i](input_deep).unsqueeze(1)
                               for i, input_deep in enumerate(customer_deep_in)]
        
        customer_deep_out = torch.cat(customer_deep_embedding_list, dim=2).squeeze(1)
        
        
        # Customer: Wide
        customer_wide_in_list = [wide_i.float() for wide_i in customer_wide_in]
        customer_wide_cat = torch.stack(customer_wide_in_list, dim=0)
        customer_wide_out = torch.transpose(customer_wide_cat, dim1=1, dim0=0)
        
        
        # Customer: Normalize
        customer_wide_out = self.customer_wide_batch_norm(customer_wide_out)


        
        #-------------------
        # Agent
        #-------------------
        
        # Agent: Deep
        agent_deep_embedding_list = [self.agent_deep_embedding[i](input_deep).unsqueeze(1)
                               for i, input_deep in enumerate(agent_deep_in)]
        
        agent_deep_out = torch.cat(agent_deep_embedding_list, dim=2).squeeze(1)
        
        
        # Agent: Wide
        agent_wide_in_list = [wide_i.float() for wide_i in agent_wide_in]
        agent_wide_cat = torch.stack(agent_wide_in_list, dim=0)
        agent_wide_out = torch.transpose(agent_wide_cat, dim1=1, dim0=0)
        
        
        # Agent: Normalize
        agent_wide_out = self.agent_wide_batch_norm(agent_wide_out)
        
        
        
        
        #-------------------------------------------
        # Tower 1:  Call-customer tower (Dynamic)
        #-------------------------------------------
        call_customer_out = torch.cat((call_wide_out, call_deep_out, customer_wide_out, customer_deep_out), dim=1) 
        
        call_customer_out = self.call_customer_dense1   (call_customer_out) 
        call_customer_out = self.call_customer_act1     (call_customer_out) 
        call_customer_out = self.call_customer_dropout1 (call_customer_out) 
        
        call_customer_out = self.call_customer_dense2   (call_customer_out) 
        call_customer_out = self.call_customer_act2     (call_customer_out) 
        call_customer_out = self.call_customer_dropout2 (call_customer_out) 
        
        
        
        #print(f"\n     search_nlp_out size: {search_nlp_out.size()}")
        #print(f"  nlp_similarity_out size: {nlp_similarity_out.size()}")
        #print(f"            user_out size: {user_out.size()}")
        #print(f"        nonquery_out size: {nonquery_out.size()}")
        #print(f"    user_context_out size: {user_context_out.size()}")
        
        
        call_customer_out = self.call_customer_dense3   (call_customer_out) 
        call_customer_out = self.call_customer_act3     (call_customer_out) 
        call_customer_out = self.call_customer_dropout3 (call_customer_out) # <=== Call & Customer embedding
        
        call_customer_embedding = call_customer_out

        
        
        #-------------------------------------
        # Tower 2: Agent tower (Static)
        #-------------------------------------
        agent_out = torch.cat((agent_wide_out, agent_deep_out), dim=1) 
        
        agent_out = self.agent_dense1   (agent_out) 
        agent_out = self.agent_act1     (agent_out) 
        agent_out = self.agent_dropout1 (agent_out) 
        
        agent_out = self.agent_dense2   (agent_out) 
        agent_out = self.agent_act2     (agent_out) 
        agent_out = self.agent_dropout2 (agent_out) 
        
        agent_out = self.agent_dense3   (agent_out) 
        agent_out = self.agent_act3     (agent_out) 
        agent_out = self.agent_dropout3 (agent_out) # <=== Agent embedding 

        agent_embedding = agent_out
        
        
        
        # Model 1: Classifier
        #outs = torch.cat((seq_out, ctx_out, search_out, next_item_out), dim=1)  # Dmitri
        #outs = self.dense1(outs) # Dmitri
        #outs = self.dense2(outs) # Dmitri
        #outs = self.activation(outs) # Dmitri
        
        
        
        # Model 2: Cross
        outs = torch.mul(call_customer_out, agent_out)
        outs = torch.sum(outs, dim=1)
        
        outs = self.final_activation(outs)  # Binary Classification
        
        model_prediction = outs
        
        #print(self.dmitri_str)
        #assert(False)
        
        
        return model_prediction, call_customer_embedding, agent_embedding
        

#==========================================================================================================================
# Search Ranking Model
#==========================================================================================================================
class GRec5(nn.Module):
    
    
    def __init__(
        self, 
        deep_dims, 
        page_dim, 
        seq_dim, 
        item_meta_dim, 
        page_embed_dim, 
        seq_embed_dim, 
        item_embed_dim, 
        item_meta_embed_dim, 
        item_pre_embed_dim, 
        deep_embed_dims, 
        wad_embed_dim, 
        nlp_embed_dim, 
        seq_hidden_size, 
        nlp_encoder_path,  
        num_wide=0, 
        num_meta_wide=0, 
        num_shared=0, 
        nlp_dim=0, 
        item_freeze=None, 
        item_pre_freeze=None, 
        nlp_freeze=None, 
        context_head_kwargs=None, 
        sequence_transformer_kwargs=None,
        page_embedding_weight=None, 
        item_embedding_weight=None, 
        item_nlp_embedding_weight=None,  # Dmitri
        item_meta_embedding_weight=None, 
        item_pre_embedding_weight=None, 
        shared_embeddings_weight=None, 
        mmoe_kwargs=None):
        super().__init__()
        
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        
        
        # --------------------------------------------------------------------------------
        # Dmitri: handle item NLP embedding weights from the NLP encoder (such as e5-base-v2)
        # --------------------------------------------------------------------------------
        if item_nlp_embedding_weight is None:  # Dmitri
            assert(False)                      # Dmitri 
        self.item_nlp_embedding = nn.Embedding.from_pretrained(item_nlp_embedding_weight, freeze=True)  # Dmitri
        #self.item_nlp_embedding.weight.requires_grad = False
        # --------------------------------------------------------------------------------
        
        
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if True: #nlp_freeze:  # Dmitri ************* FIX THIS **************
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False

        
        # ================================================
        # Dmitri
        # ================================================
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim # + item_embed_dim  # Dmitri: added item_embed_dim
        
        
        # Item Embedding
        self.next_item_embedding = self.item_embedding # nn.Embedding(seq_dim, item_embed_dim)  # Dmitri: Model 2 (x-cross)
        #self.next_item_embedding = nn.Embedding(seq_dim, NEXT_ITEM_EMBED_NDIM)  # Dmitri: Model 2 (x-cross)
        
        
        #-------------------------------------
        # Tower 1:  User-query tower (Dynamic)
        #-------------------------------------
        self.user_dense1   = torch.nn.Linear(in_features=nlp_dim, out_features=nlp_dim // 2) # 768 -> 384
        self.user_act1     = nn.LeakyReLU(0.2)
        self.user_dropout1 = nn.Dropout(p=0.1)   
        
        self.user_dense2   = torch.nn.Linear(in_features=nlp_dim // 2, out_features=item_embed_dim) # 384 -> 192
        #self.user_dense2   = torch.nn.Linear(in_features=self.combined_dim // 2, out_features=NEXT_ITEM_EMBED_NDIM)
        self.user_act2     = nn.LeakyReLU(0.2)
        self.user_dropout2 = nn.Dropout(p=0.1) 
        
        self.user_context_dense = torch.nn.Linear(in_features=wad_embed_dim + seq_embed_dim, out_features=1) # 
        
        self.user_dense3   = torch.nn.Linear(in_features=item_embed_dim + 1, out_features=item_embed_dim) # 192+1 -> 192
        self.user_act3     = nn.LeakyReLU(0.2)
        self.user_dropout3 = nn.Dropout(p=0.1) 
        
        
        
        #-------------------------------------
        # Tower 2: Item tower (Static)
        #-------------------------------------
        self.search_item_dense1   = torch.nn.Linear(in_features=nlp_dim, out_features=nlp_dim // 2) # 768 -> 384
        self.search_item_act1     = nn.LeakyReLU(0.2)
        self.search_item_dropout1 = nn.Dropout(p=0.1)   
        
        self.search_item_dense2   = torch.nn.Linear(in_features=nlp_dim // 2, out_features=item_embed_dim) # 384 -> 192
        #self.search_item_dense2   = torch.nn.Linear(in_features=self.combined_dim // 2, out_features=NEXT_ITEM_EMBED_NDIM)
        self.search_item_act2     = nn.LeakyReLU(0.2)
        self.search_item_dropout2 = nn.Dropout(p=0.1) 
        
        self.search_item_dense3   = torch.nn.Linear(in_features=item_embed_dim, out_features=item_embed_dim) # 192 -> 192
        self.search_item_act3     = nn.LeakyReLU(0.2)
        self.search_item_dropout3 = nn.Dropout(p=0.1) 


        
        
        
        
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_hidden_size,
            dim_head=seq_hidden_size,
            **sequence_transformer_kwargs
        )
#         self.att_pooling = ParallelTransformerBlock(
#             dim=256, dim_head=256, heads=1
#         )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_hidden_size,
            out_features=seq_embed_dim
        )
        #self.nlp_dense = torch.nn.Linear(
        #    in_features=nlp_dim,
        #    out_features=nlp_embed_dim
        #)
        
        
        # ================================================
        # Dmitri
        # ================================================
        
        # Dmitri #1
        #self.dense1 = torch.nn.Linear(
        #    in_features=self.combined_dim, 
        #    out_features=self.combined_dim // 2)
        
        # Dmitri #2
        #self.dense2 = torch.nn.Linear(
        #    in_features=self.combined_dim // 2, 
        #    out_features=1)

        # Dmitri #3   
        self.out_activation = torch.nn.Sigmoid()
        
        # Dmitri: Remove MMoE
        #self.mmoe = MMoE(
        #    input_size=self.combined_dim,
        #    task_num=2, 
        #    expert_hidden_sizes=[
        #        self.combined_dim,
        #        self.combined_dim // 2
        #    ],
        #    task_hidden_sizes=[
        #        [seq_dim],
        #        [9],
        #    ],
        #    **mmoe_kwargs
        #)
        
        self.seq_dim = seq_dim
        
        
    def average_pool(self, last_hidden_states,
                 attention_mask):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
    
    
    # Dmitri: modified __getitem__(self, idx) to include next_item_in
    def forward(
        self, 
        deep_in, 
        page_in, 
        item_in, 
        next_item_in, 
        vl_in, 
        item_meta_in=None, 
        page_meta_in=None, 
        item_meta_wide_in=None, 
        page_meta_wide_in=None, 
        wide_in=None, 
        input_ids=None, 
        attention_mask=None, 
        shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        
        
        #search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)  # Dmitri
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask)
        search_nlp_out = self.average_pool(search_out.last_hidden_state, attention_mask)  # Dmitri
        #search_out = self.nlp_dense(search_out)  # Dmitri
        
        
        
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(
            page_in=page_in, 
            item_in=item_in, 
            item_meta_in=item_meta_in, 
            page_meta_in=page_meta_in, 
            item_meta_wide_in=item_meta_wide_in, 
            page_meta_wide_in=page_meta_wide_in, 
            vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        
        # ================================================
        # Dmitri
        # ================================================
        # Method1: don't use outs x item_out  (Implemented below)
        # Method2:       use outs x item_out  (Not used)
        
        #item_out = self.item_embedding(item_in.long()).squeeze(1) # Dmitri. 
        #next_item_out = self.next_item_embedding(next_item_in) # Dmitri. 
        #next_item_out = self.item_embedding(next_item_in.long()).squeeze(1) # Dmitri 
        
        next_item_nlp_out = self.item_nlp_embedding(next_item_in.long()).squeeze(1) # Dmitri 
        
        
        # Compute NLP similarity for (qeury, response)
        # Example 1: ("iphone", "iphone 14 pro max") should be similar
        # Example 2: ("iphone", "vacuum cleaner")    should not be similar
        #nlp_similarity_out = torch.mul(search_nlp_out, next_item_nlp_out)
        #nlp_similarity_out = torch.sum(nlp_similarity_out, dim=1)[:, None] # [:, None] to add 1 as last dimension [batch_size,1]
        
        #print(f"\n  item_out.dim={item_out.size()}")
        #print(f"\n  seq_out.dim={seq_out.size()}")
        
        
        #-------------------------------------
        # Tower 1:  User-query tower (Dynamic)
        #-------------------------------------
        #user_out = torch.cat((seq_out, ctx_out, search_out), dim=1) # Dmitri
        user_out = search_nlp_out # Dmitri
        
        user_out = self.user_dense1   (user_out) # Dmitri  # 768 -> 384
        user_out = self.user_act1     (user_out) # Dmitri
        user_out = self.user_dropout1 (user_out) # Dmitri
        
        user_out = self.user_dense2   (user_out) # Dmitri  # 384 -> 192 
        user_out = self.user_act2     (user_out) # Dmitri
        user_out = self.user_dropout2 (user_out) # Dmitri
        
        
        # Summarize context
        nonquery_out = torch.cat((seq_out, ctx_out), dim=1) # Dmitri 
        user_context_out = self.user_context_dense(nonquery_out) # Dmitri
        
        #print(f"\n     search_nlp_out size: {search_nlp_out.size()}")
        #print(f"  nlp_similarity_out size: {nlp_similarity_out.size()}")
        #print(f"            user_out size: {user_out.size()}")
        #print(f"        nonquery_out size: {nonquery_out.size()}")
        #print(f"    user_context_out size: {user_context_out.size()}")
        
        
        #user_out = torch.cat((nlp_similarity_out, user_out, user_context_out), dim=1) # Dmitri # 1 + 192 + 1
        user_out = torch.cat((user_out, user_context_out), dim=1) # Dmitri # 0 + 192 + 1
        
        
        user_out = self.user_dense3   (user_out) # Dmitri # 192 + 2 -> 192
        user_out = self.user_act3     (user_out) # Dmitri
        user_out = self.user_dropout3 (user_out) # Dmitri

        
        
        #-------------------------------------
        # Tower 2: Item tower (Static)
        #-------------------------------------
        search_item_out = next_item_nlp_out
        
        search_item_out = self.search_item_dense1   (search_item_out) # Dmitri # 768 -> 384
        search_item_out = self.search_item_act1     (search_item_out) # Dmitri 
        search_item_out = self.search_item_dropout1 (search_item_out) # Dmitri
        
        search_item_out = self.search_item_dense2   (search_item_out) # Dmitri # 384 -> 192
        search_item_out = self.search_item_act2     (search_item_out) # Dmitri
        search_item_out = self.search_item_dropout2 (search_item_out) # Dmitri
        
        search_item_out = self.search_item_dense3   (search_item_out) # Dmitri # 192 -> 192
        search_item_out = self.search_item_act3     (search_item_out) # Dmitri
        search_item_out = self.search_item_dropout3 (search_item_out) # Dmitri  <==== Item embedding

        # Model 1: Classifier
        #outs = torch.cat((seq_out, ctx_out, search_out, next_item_out), dim=1)  # Dmitri
        #outs = self.dense1(outs) # Dmitri
        #outs = self.dense2(outs) # Dmitri
        #outs = self.activation(outs) # Dmitri
        
        
        
        # Model 2: Cross
        outs = torch.mul(user_out, search_item_out)
        outs = torch.sum(outs, dim=1)
        outs = self.out_activation(outs)
        
        #print(self.dmitri_str)
        #assert(False)
        
        
        return outs, user_out, search_item_out
        
        
        
        # Dmitri: 
        # seq_out: tranformer out, all the behavioral data             | Sequence embedding is 256: 224 + 32 = page_embed_dim + item_meta_embed_dim
        # ctx_out: context out, this is wide and deep                  | Wide and Deep is 256
        # search_out: NLP                                              | NLP embedding is 256 (Q: Reduce this to emphasize the other parts?)
        # task_out: useless for search, as there is only 1 task
        
        
        # Dmitri

        # task1_out, task2_out = self.mmoe(outs)  # Remove this
        
        
        # TODO: 
        
        # Dense (n)
        # Dense (n//2)
        # Sigmoid
        
        # Remove task2
        
 
        #return (task1_out, task2_out)

    
class GRec(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, item_meta_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dims, task_type_embed_dim, task_out_dims, num_task,
                 num_wide=0, num_meta_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
#         self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
#         self.mm_pooling = MeanMaxPooling()
        self.task_embedding = nn.ModuleList([
            nn.Embedding(task_type_dim, task_type_embed_dim)
            for task_type_dim in task_type_dims
        ])
#         print(task_type_dims)
#         print(self.task_embedding)
#         self.task_embedding = nn.Embedding(task_type_dims, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            moe_kwargs=moe_kwargs,
            **sequence_transformer_kwargs
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
#         self.moe = MoEFFLayerTopK(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), num_K=moe_kwargs.get("num_K"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
        
#         self.moe = MoEFFLayer(dim=self.combined_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), hidden_size=self.combined_dim, expert_class=ExpertLayer)
#         self.tasks_dense1 = nn.ModuleDict()
#         self.tasks_dense2 = nn.ModuleDict()
#         self.tasks_act1 = self.tasks_act2 = nn.ModuleDict()
#         for i in range(task_type_dim):
#             self.tasks_dense1[f"task{i}_dense1"] = nn.Linear(
#                 self.combined_dim, 
#                 self.combined_dim // 2
#             )
#             self.tasks_dense2[f"task{i}_dense2"] = nn.Linear(
#                 self.combined_dim // 2, 
#                 task_out_dims[i]
#             )
#             self.tasks_act1[f"task{i}_act1"] = self.tasks_act2[f"task{i}_act2"] = nn.LeakyReLU(0.2)

        self.tasks_dense1 = nn.Linear(
            self.combined_dim, 
            self.combined_dim // 2
        )
        self.tasks_dense2 = nn.Linear(
            self.combined_dim // 2, 
            task_out_dims[0],
            bias=False
        )
        self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = num_task
#         self.awl = AutomaticWeightedLoss(task_type_dim)

#     def split_task(self, task_type_dim, task_in, combined_out):
#         task_indices = []
#         task_outs = []
#         task_user_outs = []
#         for i in range(task_type_dim):
#             task_indice = task_in == i
#             task_indice = torch.nonzero(task_indice).flatten()
#             task_input = combined_out[task_indice]
#             task_out = self.tasks_dense1[f"task{i}_dense1"](task_input)
#             task_user_out = self.tasks_act1[f"task{i}_act1"](task_out)
#             task_out = self.tasks_dense2[f"task{i}_dense2"](task_user_out)
#             task_indices.append(task_indice)
#             task_user_outs.append(task_user_out)
#             task_outs.append(task_out)
#         return task_indices, task_outs, task_user_outs
    
    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1(task_input)
            task_user_out = self.tasks_act1(task_out)
            task_out = self.tasks_dense2(task_user_out)
            task_indices.append(task_indice)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
    
    def average_pool(self, last_hidden_states, attention_mask):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
    
        
    def forward(self, deep_in, page_in, item_in, vl_in, tasks_in, current_in, current_meta_in, item_meta_in=None, page_meta_in=None, item_meta_wide_in=None, page_meta_wide_in=None, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)
#         search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)

        # search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask)
        # search_out = self.average_pool(search_out.last_hidden_state, attention_mask)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, page_meta_in=page_meta_in, item_meta_wide_in=item_meta_wide_in, page_meta_wide_in=page_meta_wide_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        current_item_out = self.item_embedding(current_in)
        current_meta_out = self.item_meta_embedding(current_meta_in)
        current_pre_out = self.item_pre_embedding(current_in)

        current_out = torch.cat((current_item_out, current_meta_out, current_pre_out), 1)

#         tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
#                            for i, task_in in enumerate(tasks_in)]
#         task_out = torch.cat(tasks_out_list, dim=2)
#         outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :]), dim=1)
#         outs = self.att_pooling(outs)
#         outs, aux_loss = self.moe(outs, task_out)
        
        
        tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
                           for i, task_in in enumerate(tasks_in)]
        task_out = torch.cat(tasks_out_list, dim=2).squeeze(1)
        # task_out = self.mm_pooling(tasks_out)
        outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :], task_out[:, None, :]), dim=1)
        outs = self.att_pooling(outs)
        outs, aux_loss = self.moe(outs)
        
        outs = outs.reshape(-1, self.combined_dim)
        task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, tasks_in[0], outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)
    
class GRecOffer2(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, item_meta_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dims, task_type_embed_dim, task_out_dims, num_task, num_offer,
                 num_wide=0, num_meta_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None, mmoe_kwargs=None):
        super().__init__()
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
#         self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
#         self.mm_pooling = MeanMaxPooling()
        self.task_embedding = nn.ModuleList([
            nn.Embedding(task_type_dim, task_type_embed_dim)
            for task_type_dim in task_type_dims
        ])
#         print(task_type_dims)
#         print(self.task_embedding)
#         self.task_embedding = nn.Embedding(task_type_dims, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            moe_kwargs=moe_kwargs,
            **sequence_transformer_kwargs
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
        self.mmoe = MMoE(
            input_size=self.combined_dim,
            expert_hidden_sizes=[
                self.combined_dim,
                self.combined_dim // 2
            ],
            task_hidden_sizes=[
                [seq_dim],
                [num_offer]
            ],
            **mmoe_kwargs
        )

        # self.tasks_dense1 = nn.Linear(
        #     self.combined_dim, 
        #     self.combined_dim // 2
        # )
        # self.tasks_dense2 = nn.Linear(
        #     self.combined_dim // 2, 
        #     task_out_dims[0],
        #     bias=False
        # )
        # self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = num_task
    
    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task1_out, task2_out = self.mmoe(task_input)
            task_indices.append(task_indice)
            task_outs.append((task1_out, task2_out))
        return task_indices, task_outs
    
    def average_pool(self, last_hidden_states, attention_mask):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
    
        
    def forward(self, deep_in, page_in, item_in, vl_in, tasks_in, current_in, current_meta_in, item_meta_in=None, page_meta_in=None, item_meta_wide_in=None, page_meta_wide_in=None, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)
#         search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)

        # search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask)
        # search_out = self.average_pool(search_out.last_hidden_state, attention_mask)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, page_meta_in=page_meta_in, item_meta_wide_in=item_meta_wide_in, page_meta_wide_in=page_meta_wide_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        current_item_out = self.item_embedding(current_in)
        current_meta_out = self.item_meta_embedding(current_meta_in)
        current_pre_out = self.item_pre_embedding(current_in)

        current_out = torch.cat((current_item_out, current_meta_out, current_pre_out), 1)

#         tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
#                            for i, task_in in enumerate(tasks_in)]
#         task_out = torch.cat(tasks_out_list, dim=2)
#         outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :]), dim=1)
#         outs = self.att_pooling(outs)
#         outs, aux_loss = self.moe(outs, task_out)
        
        
        tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
                           for i, task_in in enumerate(tasks_in)]
        task_out = torch.cat(tasks_out_list, dim=2).squeeze(1)
        # task_out = self.mm_pooling(tasks_out)
        outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :], task_out[:, None, :]), dim=1)
        outs = self.att_pooling(outs)
        outs, aux_loss = self.moe(outs)
        
        outs = outs.reshape(-1, self.combined_dim)
        task_indices, task_outs = self.split_task(self.task_type_dim, tasks_in[0], outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)
    

class GRecOffer(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, item_meta_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dims, task_type_embed_dim, task_out_dims, num_task, num_offer,
                 num_wide=0, num_meta_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
#         self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
#         self.mm_pooling = MeanMaxPooling()
        self.task_embedding = nn.ModuleList([
            nn.Embedding(task_type_dim, task_type_embed_dim)
            for task_type_dim in task_type_dims
        ])
#         print(task_type_dims)
#         print(self.task_embedding)
#         self.task_embedding = nn.Embedding(task_type_dims, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            moe_kwargs=moe_kwargs,
            **sequence_transformer_kwargs
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
        self.tasks_dense1 = nn.Linear(
            self.combined_dim, 
            self.combined_dim // 2
        )
        self.tasks_dense2 = nn.Linear(
            self.combined_dim // 2, 
            task_out_dims[0],
            bias=False
        )
        self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = num_task
    
    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1(task_input)
            task_user_out = self.tasks_act1(task_out)
            task_out = self.tasks_dense2(task_user_out)
            task_indices.append(task_indice)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
    
    def average_pool(self, last_hidden_states, attention_mask):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
    
        
    def forward(self, deep_in, page_in, item_in, vl_in, tasks_in, current_in, current_meta_in, item_meta_in=None, page_meta_in=None, item_meta_wide_in=None, page_meta_wide_in=None, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)
#         search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)

        # search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask)
        # search_out = self.average_pool(search_out.last_hidden_state, attention_mask)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, page_meta_in=page_meta_in, item_meta_wide_in=item_meta_wide_in, page_meta_wide_in=page_meta_wide_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        current_item_out = self.item_embedding(current_in)
        current_meta_out = self.item_meta_embedding(current_meta_in)
        current_pre_out = self.item_pre_embedding(current_in)

        current_out = torch.cat((current_item_out, current_meta_out, current_pre_out), 1)

#         tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
#                            for i, task_in in enumerate(tasks_in)]
#         task_out = torch.cat(tasks_out_list, dim=2)
#         outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :]), dim=1)
#         outs = self.att_pooling(outs)
#         outs, aux_loss = self.moe(outs, task_out)
        
        
        tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
                           for i, task_in in enumerate(tasks_in)]
        task_out = torch.cat(tasks_out_list, dim=2).squeeze(1)
        # task_out = self.mm_pooling(tasks_out)
        outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :], task_out[:, None, :]), dim=1)
        outs = self.att_pooling(outs)
        outs, aux_loss = self.moe(outs)
        
        outs = outs.reshape(-1, self.combined_dim)
        task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, tasks_in[0], outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)
    

class GRec2(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, item_meta_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dims, task_type_embed_dim, task_out_dims, num_task,
                 num_wide=0, num_meta_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
#         self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim
#         self.mm_pooling = MeanMaxPooling()
        self.task_embedding = nn.ModuleList([
            nn.Embedding(task_type_dim, task_type_embed_dim)
            for task_type_dim in task_type_dims
        ])
#         print(task_type_dims)
#         print(self.task_embedding)
#         self.task_embedding = nn.Embedding(task_type_dims, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            moe_kwargs=moe_kwargs,
            **sequence_transformer_kwargs
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
        self.mmoe = MMoE(
            input_size=combined_dim,
            task_num=2, 
            expert_hidden_sizes=[
                self.combined_dim,
                self.combined_dim // 2
            ],
            task_hidden_sizes=[
                [task_out_dims[0]],
                [3],
            ],
            **mmoe_kwargs
        )
        self.tasks_dense1 = nn.Linear(
            self.combined_dim, 
            self.combined_dim // 2
        )
        self.tasks_dense2 = nn.Linear(
            self.combined_dim // 2, 
            task_out_dims[0]
        )
        self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = num_task
    
    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1(task_input)
            task_user_out = self.tasks_act1(task_out)
            task_out = self.tasks_dense2(task_user_out)
            task_indices.append(task_indice)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
        
    def forward(self, deep_in, page_in, item_in, vl_in, tasks_in, item_meta_in=None, page_meta_in=None, item_meta_wide_in=None, page_meta_wide_in=None, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)
#         search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, page_meta_in=page_meta_in, item_meta_wide_in=item_meta_wide_in, page_meta_wide_in=page_meta_wide_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        outs = torch.cat((seq_out, ctx_out, search_out), dim=0)
        task1_out, task2_out = self.mmoe(outs)
        
#         tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
#                            for i, task_in in enumerate(tasks_in)]
#         task_out = torch.cat(tasks_out_list, dim=2).squeeze(1)
# #         task_out = self.mm_pooling(tasks_out)
#         outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], task_out[:, None, :]), dim=1)
#         outs = self.att_pooling(outs)
#         outs, aux_loss = self.moe(outs)
        
#         outs = outs.reshape(-1, self.combined_dim)
#         task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, tasks_in[0], outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)


class GRec3(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, item_meta_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, num_intent, num_wide=0, num_meta_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, mmoe_kwargs=None):
        super().__init__()
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False

        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_hidden_size,
            dim_head=seq_hidden_size,
            **sequence_transformer_kwargs
        )
#         self.att_pooling = ParallelTransformerBlock(
#             dim=256, dim_head=256, heads=1
#         )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_hidden_size,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.mmoe = MMoE(
            input_size=self.combined_dim,
            expert_hidden_sizes=[
                self.combined_dim,
                self.combined_dim // 2
            ],
            task_hidden_sizes=[
                [seq_dim],
                [num_intent]
            ],
            **mmoe_kwargs
        )
        self.seq_dim = seq_dim
        
    def average_pool(self, last_hidden_states,
                 attention_mask):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
        
    def forward(self, deep_in, page_in, item_in, vl_in, item_meta_in=None, page_meta_in=None, item_meta_wide_in=None, page_meta_wide_in=None, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)
#         search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask)
#         search_out = self.average_pool(search_out.last_hidden_state, attention_mask)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, page_meta_in=page_meta_in, item_meta_wide_in=item_meta_wide_in, page_meta_wide_in=page_meta_wide_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        outs = torch.cat((seq_out, ctx_out, search_out), dim=1)
        task1_out, task2_out = self.mmoe(outs)
 
        return (task1_out, task2_out)


class PaRSAudienceTT(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, item_dim,
                 seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs,
                 user_moe_kwargs, offer_moe_kwargs, task_type_dim):
        super().__init__()
        self.task_type_dim = task_type_dim
        self.seq_embed_dim = seq_embed_dim

        # user layers
        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        self.user_task_type_embedding = nn.Embedding(task_type_dim, seq_embed_dim)
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim \
                               + seq_embed_dim + seq_embed_dim + seq_embed_dim
        self.user_moe = MoEFFLayer(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            # num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_dense_0 = nn.ModuleDict()
        self.user_dense_1 = nn.ModuleDict()
        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        for i in range(task_type_dim):
            self.user_dense_0[f"task{i}_dense1"] = nn.Linear(
                in_features=self.user_concat_dim,
                out_features=seq_embed_dim * 3
            )
            self.user_dense_1[f"task{i}_dense2"] = nn.Linear(
                in_features=seq_embed_dim * 3,
                out_features=seq_embed_dim
            )

        # offer layers
        self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )
        self.offer_task_type_embedding = nn.Embedding(task_type_dim, seq_embed_dim)
        self.offer_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # offer_context_out
        self.offer_concat_dim = seq_embed_dim + seq_embed_dim
        self.offer_moe = MoEFFLayer(
            dim=seq_embed_dim,
            num_experts=offer_moe_kwargs.get("num_experts"),
            expert_capacity=offer_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            # num_K=offer_moe_kwargs.get("num_K"),
        )

        self.offer_dense_0 = nn.ModuleDict()
        self.offer_dense_1 = nn.ModuleDict()
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)
        for i in range(task_type_dim):
            self.offer_dense_0[f"task{i}_dense1"] = nn.Linear(
                in_features=self.offer_concat_dim,
                out_features=self.offer_concat_dim + self.offer_concat_dim // 2
            )
            self.offer_dense_1[f"task{i}_dense2"] = nn.Linear(
                in_features=self.offer_concat_dim + self.offer_concat_dim // 2,
                out_features=seq_embed_dim
            )

        self.out_act = nn.Sigmoid()

    def user_split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(self.task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_indices.append(task_indice)
            task_input = combined_out[task_indice]
            task_out = self.user_dense_0[f"task{i}_dense1"](task_input)
            task_out = self.user_act(task_out)
            task_out = self.user_dropout(task_out)
            task_out = self.user_dense_1[f"task{i}_dense2"](task_out)
            task_out = self.user_act(task_out)
            task_outs.append(task_out)
        return task_indices, task_outs

    def offer_split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(self.task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_indices.append(task_indice)
            task_input = combined_out[task_indice]
            task_out = self.offer_dense_0[f"task{i}_dense1"](task_input)
            task_out = self.offer_act(task_out)
            task_out = self.offer_dropout(task_out)
            task_out = self.offer_dense_1[f"task{i}_dense2"](task_out)
            task_out = self.offer_act(task_out)
            task_outs.append(task_out)
        return task_indices, task_outs

    def forward(self, user_deep_in, offer_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in,
                user_wide_in, offer_wide_in, search_in, task_type_in):
        device = vl_in.device

        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_task_out = self.user_task_type_embedding(task_type_in.long())
        user_out = torch.stack([user_task_out, search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
#         user_task_out_routing = user_task_out[:, None, :]
#         user_task_out_routing = torch.cat([user_task_out_routing] * user_out.shape[1], dim=1)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_task_indices, user_outs = self.user_split_task(task_type_in, user_out)
        user_out_res = torch.zeros(user_out.shape[0], self.seq_embed_dim).to(device)
        for i in range(self.task_type_dim):
            user_out_res[user_task_indices[i]] = user_outs[i]

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_task_out = self.offer_task_type_embedding(task_type_in.long())
        offer_out = torch.stack([offer_task_out, offer_ctx_out], dim=1)
        offer_out = self.offer_att_pooling(offer_out)
#         offer_task_out_routing = offer_task_out[:, None, :]
#         offer_task_out_routing = torch.cat([offer_task_out_routing] * offer_out.shape[1], dim=1)
        offer_out, offer_aux_loss = self.offer_moe(offer_out)
        offer_out = offer_out.reshape(-1, self.offer_concat_dim)
        offer_task_indices, offer_outs = self.offer_split_task(task_type_in, offer_out)
        offer_out_res = torch.zeros(offer_out.shape[0], self.seq_embed_dim).to(device)
        for i in range(self.task_type_dim):
            offer_out_res[offer_task_indices[i]] = offer_outs[i]

        out = torch.mul(user_out_res, offer_out_res)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out_res, offer_out_res, (user_aux_loss, offer_aux_loss)


class GRecSingleTaskTT(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, item_dim,
                 seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs,
                 user_moe_kwargs):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        # user layers
        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim \
                               + seq_embed_dim + seq_embed_dim
        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=seq_embed_dim * 3
        )
        self.user_dense_1 = nn.Linear(
            in_features=seq_embed_dim * 3,
            out_features=seq_embed_dim
        )

        # offer layers
        self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )
        # offer_context_out
        self.offer_concat_dim = seq_embed_dim
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)
        self.offer_dense_0 = nn.Linear(
            in_features=self.offer_concat_dim,
            out_features=self.offer_concat_dim + self.offer_concat_dim // 2
        )
        self.offer_dense_1 = nn.Linear(
            in_features=self.offer_concat_dim + self.offer_concat_dim // 2,
            out_features=seq_embed_dim
        )

        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, offer_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in,
                user_wide_in, offer_wide_in, search_in):
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

#        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.stack([search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = offer_ctx_out
        offer_out = self.offer_dense_0(offer_out)
        offer_out = self.offer_act(offer_out)
        offer_out = self.offer_dropout(offer_out)
        offer_out = self.offer_dense_1(offer_out)
        offer_out = self.offer_act(offer_out)

        out = torch.mul(user_out, offer_out)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out, offer_out, user_aux_loss


class GRecUPG(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, item_dim,
                 seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs,
                 user_moe_kwargs):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        # user layers
        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim \
                               + seq_embed_dim + seq_embed_dim
        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=seq_embed_dim * 3
        )
        self.user_dense_1 = nn.Linear(
            in_features=seq_embed_dim * 3,
            out_features=seq_embed_dim
        )

        self.out_dense = nn.Linear(
            in_features=seq_embed_dim,
            out_features=1
        )
        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in,
                user_wide_in, search_in):
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.stack([search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        out = self.out_dense(user_out)
        out = self.out_act(out)

        return out, user_aux_loss

    
class PaRS2(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dim, task_type_embed_dim, task_out_dims, num_wide=0, num_shared=0, nlp_dim=0, page_meta_dim=0, page_meta_embed_dim=0, num_page_meta_wide=0, page_meta_wide_embed_dim=0, num_item_meta_wide=0, item_meta_wide_embed_dim=0, page_freeze=None, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None, page_embedding_weight=None, page_meta_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if page_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_meta_embedding = nn.Embedding(page_meta_dim, page_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_meta_embedding = nn.Embedding.from_pretrained(page_meta_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
        if page_freeze:
            self.page_embedding.weight.requires_grad = False
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False

        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
        self.task_embedding = nn.Embedding(task_type_dim, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP3(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
            num_page_meta_wide=num_page_meta_wide,
            num_item_meta_wide=num_item_meta_wide,
            page_meta_embedding=self.page_meta_embedding,
            page_meta_wide_embed_dim=page_meta_wide_embed_dim,
            item_meta_wide_embed_dim=item_meta_wide_embed_dim,
            moe_kwargs=moe_kwargs
        )
    
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)

        self.tasks_dense1 = nn.Linear(
            self.combined_dim, 
            self.combined_dim // 2
        )
        self.tasks_dense2 = nn.Linear(
            self.combined_dim // 2, 
            task_out_dims[0]
        )
        self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = task_type_dim

        if num_item_meta_wide > 0:
            self.wide_meta_batch_norm = nn.BatchNorm1d(num_item_meta_wide)
            if item_meta_wide_embed_dim > 0:
                self.wide_meta_dense = nn.Linear(num_item_meta_wide, item_meta_wide_embed_dim)
            else: 
                print("There are wide meta features but item_meta_wide_embed_dim is not given!")
            self.wide_meta_act = nn.LeakyReLU(0.2)

    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1(task_input)
            task_user_out = self.tasks_act1(task_out)
            task_out = self.tasks_dense2(task_user_out)
            task_indices.append(task_indice)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
        
    def forward(self, deep_in, page_in, item_in, item_meta_in, vl_in, task_in, current_in, current_meta_in, wide_in=None, input_ids=None, attention_mask=None, page_meta_in=None, page_meta_wide_in=None, current_meta_wide_in=None, item_meta_wide_in=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of tensor of shape [batch_size, deep_dims]
            page_in: tensor, page input sequence [batch_size, seq_len]
            item_in: tensor, item input sequence [batch_size, seq_len]
            item_meta_in: tensor, item deep meta data input sequence [batch_size, seq_len]
            vl_in: tensor, valid length of input data [batch_size]
            taks_in: tensor, task type index [batch_size]
            current_in: tensor, current item input [batch_size]
            current_meta_in: tensor, current item deep meta data input [batch_size]
            wide_in: list, a list of tensor of shape [batch_size, num_wide]
            inputs_id: list, a list of tensor of shape [batch_size, num_shared] (default=None)
            att_mask: tensor, tensor of shape [batch_size, sentence_length] (default=None)
            page_meta_in: tensor, page deep meta data input sequence [batch_size, seq_len]
            page_meta_wide_in: tensor, page wide meta data input sequence [batch_size, num_page_meta_wide, seq_len]
            current_meta_wide_in: list, a list of tensor of shape [batch_size, num_item_meta_wide]
            item_meta_wide_in: tensor, item wide meta data input sequence [batch_size, num_item_meta_wide, seq_len]
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None)

        Return:
            out: tensor, shape [batch_size, seq_dim].
            user_out: tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, vl_in=vl_in, page_meta_in=page_meta_in, page_meta_wide_in=page_meta_wide_in, item_meta_wide_in=item_meta_wide_in)
        seq_out = self.seq_dense(seq_out)
        current_item_out = self.item_embedding(current_in)
        current_meta_out = self.item_meta_embedding(current_meta_in)
        current_pre_out = self.item_pre_embedding(current_in)	        
        if current_meta_wide_in is not None:
            current_meta_wide_in_list = [wide_i.float() for wide_i in current_meta_wide_in]
            current_meta_wide_cat = torch.stack(current_meta_wide_in_list, dim=0)
            current_meta_wide_out = torch.transpose(current_meta_wide_cat, dim1=1, dim0=0)
            if len(current_meta_wide_in) > 1:
                current_meta_wide_out_norm = self.wide_meta_batch_norm(current_meta_wide_out)
            else:
                current_meta_wide_out_norm = current_meta_wide_out
            current_meta_wide_out_norm = self.wide_meta_dense(current_meta_wide_out_norm)
            current_meta_wide_out_norm = self.wide_meta_act(current_meta_wide_out_norm)
            current_out = torch.cat((current_item_out, current_meta_out, current_pre_out, current_meta_wide_out_norm), 1)
        else:
            current_out = torch.cat((current_item_out, current_meta_out, current_pre_out), 1)
        
        task_out = self.task_embedding(task_in)
        outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :], task_out[:, None, :]), dim=1)
        outs = self.att_pooling(outs)
        outs, aux_loss = self.moe(outs)
        
        outs = outs.reshape(-1, self.combined_dim)
        task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, task_in, outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)


class GRecBillshock(nn.Module):
    def __init__(self, deep_dims, deep_embed_dims, num_wide, wad_embed_dim,
                 shared_embeddings_weight=None, moe_kwargs=None):
        
        super().__init__()

        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        
#         self.att_pooling = ParallelTransformerBlock(
#             dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
#         )

        self.concat_dim = wad_embed_dim 
        
        self.moe = MoEFFLayerTopK(
            dim=self.concat_dim,
            num_experts=moe_kwargs.get("num_experts"),
            expert_capacity=moe_kwargs.get("expert_capacity"),
            hidden_size=self.concat_dim,
            expert_class=ExpertLayer,
            num_K=moe_kwargs.get("num_K"),
        )

        self.act = nn.LeakyReLU(0.2)
        self.dropout = nn.Dropout(p=0.2)
        self.dense_0 = nn.Linear(
            in_features=self.concat_dim,
            out_features=self.concat_dim * 3
        )
        self.dense_1 = nn.Linear(
            in_features=self.concat_dim* 3,
            out_features=self.concat_dim
        )

        self.out_dense = nn.Linear(
            in_features=self.concat_dim,
            out_features=1
        )
        self.out_act = nn.Sigmoid()

    def forward(self, deep_in, wide_in):
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in)
        out = ctx_out[:, None, :]
#        out = self.att_pooling(out)
        out, aux_loss = self.moe(out)
        out = out.reshape(-1, self.concat_dim)
        out = self.dense_0(out)
        out = self.act(out)
        out = self.dropout(out)
        out = self.dense_1(out)
        out = self.act(out)

        out = self.out_dense(out)
        out = self.out_act(out)

        return out, aux_loss


class GRecBillshock2(nn.Module):
    def __init__(self, deep_dims, deep_embed_dims, num_wide, wad_embed_dim,
                 moe_kwargs=None):
        
        super().__init__()

        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        
        self.concat_dim = wad_embed_dim

        self.act = nn.LeakyReLU(0.2)
        self.dropout = nn.Dropout(p=0.2)
        self.dense_0 = nn.Linear(
            in_features=self.concat_dim,
            out_features=self.concat_dim * 3
        )
        self.dense_1 = nn.Linear(
            in_features=self.concat_dim* 3,
            out_features=self.concat_dim
        )

        self.out_dense = nn.Linear(
            in_features=self.concat_dim,
            out_features=1
        )
        self.out_act = nn.Sigmoid()

    def forward(self, deep_in, wide_in):
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in)
        out = self.dense_0(ctx_out)
        out = self.act(out)
        out = self.dropout(out)
        out = self.dense_1(out)
        out = self.act(out)

        out = self.out_dense(out)
        out = self.out_act(out)

        return out


class GRecSingleTaskTT2(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 page_dim, item_dim, seq_embed_dim, sequence_transformer_kwargs, user_moe_kwargs,
                 nlp_dim=0, offer_deep_embed_dims=0, offer_num_wide=0, offer_wad_embed_dim=0,
                 nlp_encoder_path=None, offer_deep_dims=None, other_seq_num=None, other_seq_embed_dim=None):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        ## user layers
        if other_seq_num:
            self.seq_embedding = dict()
            for i in range(len(other_seq_num)):
                self.seq_embedding[i] = nn.Embedding(other_seq_num[i], other_seq_embed_dim[i] )
            #self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
            #self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
            self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        if nlp_dim > 0:
            #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
            self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
            self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
            )
            self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
            )
            self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        
        if nlp_dim > 0:
            if other_seq_num:
                # nlp_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + len(self.seq_embedding) * seq_embed_dim
            else:
                # nlp_out + aep_seq_out + user_ctx_out 
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim 
        else:
            if other_seq_num:
                # aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + len(self.seq_embedding) * seq_embed_dim
            else:
                # aep_seq_out + user_ctx_out 
                self.user_concat_dim = seq_embed_dim + seq_embed_dim 
                
        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=seq_embed_dim * 3
        )
        self.user_dense_1 = nn.Linear(
            in_features=seq_embed_dim * 3,
            out_features=seq_embed_dim
        )

        ## offer layers
        if offer_deep_dims:
            self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
            )
            # offer_context_out
            self.offer_concat_dim = seq_embed_dim
            self.offer_act = nn.LeakyReLU(0.2)
            self.offer_dropout = nn.Dropout(p=0.1)
            if offer_num_wide>0:
                self.offer_dense_0 = nn.Linear(
                in_features=offer_wad_embed_dim//2 + offer_wad_embed_dim//2,
                out_features=self.offer_concat_dim + self.offer_concat_dim // 2
                )
            else:
                self.offer_dense_0 = nn.Linear(
                in_features=offer_wad_embed_dim//2,
                out_features=self.offer_concat_dim + self.offer_concat_dim // 2
                )
            self.offer_dense_1 = nn.Linear(
                in_features=self.offer_concat_dim + self.offer_concat_dim // 2,
                out_features=seq_embed_dim
            )

        self.out_act = nn.Sigmoid()
        self.seq_out = {}

    def forward(self, user_deep_in, page_in, item_in, vl_in, user_wide_in, 
                search_in = None, offer_deep_in = None, offer_wide_in = None, 
                sequence_in = None):
        
#         svc_out = self.svc_embedding(svc_in.long())
#         svc_out = self.mm_pooling(svc_out)
#         new_svc_out = self.new_svc_embedding(new_svc_in.long())
#         new_svc_out = self.mm_pooling(new_svc_out)
        
        device = vl_in.device
        
        if sequence_in:
            sequence_out = []
            for i in range(len(sequence_in)):
                self.seq_embedding[i] = self.seq_embedding[i].to(device)
                sequence_out.append(self.mm_pooling(self.seq_embedding[i](sequence_in[i].long())))
        
        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        if search_in:
#        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
            search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
            search_out = self.search_nlp_dense_0(search_out)
            search_out = self.nlp_act(search_out)
            search_out = self.search_nlp_dense_1(search_out)
            search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        
        if search_in:
            if sequence_in:
                user_out = torch.stack([search_out, aep_seq_out, user_ctx_out] + sequence_out, dim=1)
            else:
                user_out = torch.stack([search_out, aep_seq_out, user_ctx_out], dim=1)
        else:
            if sequence_in:
                user_out = torch.stack([aep_seq_out, user_ctx_out] + sequence_out, dim=1)
            else:
                user_out = torch.stack([aep_seq_out, user_ctx_out] , dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)
        
        if offer_deep_in:
            offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
            offer_out = offer_ctx_out
            offer_out = self.offer_dense_0(offer_out)
            offer_out = self.offer_act(offer_out)
            offer_out = self.offer_dropout(offer_out)
            offer_out = self.offer_dense_1(offer_out)
            offer_out = self.offer_act(offer_out)

            out = torch.mul(user_out, offer_out)
        else:
            out = user_out
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        if offer_deep_in:
            return out, user_out, offer_out, user_aux_loss
        else:
            return out, user_out, user_aux_loss


class GRecUserMultiLabel(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 page_dim, item_dim, seq_embed_dim, sequence_transformer_kwargs, user_moe_kwargs,
                 task_type_dims=(1, 140), nlp_dim=0, nlp_encoder_path=None, other_seq_num=None, other_seq_embed_dim=None):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        ## user layers
        if other_seq_num:
            self.seq_embedding = nn.ModuleList()
            for i in range(len(other_seq_num)):
                self.seq_embedding.append(nn.Embedding(other_seq_num[i], other_seq_embed_dim[i]))
            # self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
            # self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
            self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        if nlp_dim > 0:
            # self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
            self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
            self.search_nlp_dense_0 = torch.nn.Linear(
                in_features=nlp_dim,
                out_features=seq_embed_dim * 2
            )
            self.search_nlp_dense_1 = torch.nn.Linear(
                in_features=seq_embed_dim * 2,
                out_features=seq_embed_dim
            )
            self.nlp_act = nn.LeakyReLU(0.2)

       # self.user_context_head = ContextTransformerAndWide(
        self.user_context_head = ContextHead(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )

        if nlp_dim > 0:
            if other_seq_num:
                # task_type_out + nlp_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim + len(
                    other_seq_num) * seq_embed_dim
            else:
                # task_type_out + nlp_out + aep_seq_out + user_ctx_out
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
        else:
            if other_seq_num:
                # task_type_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + len(other_seq_num) * seq_embed_dim
            else:
                # task_type_out + aep_seq_out + user_ctx_out
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim

        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )

        ## task layers
        self.task_type_dims = task_type_dims
        self.task_type_embedding = nn.Embedding(len(task_type_dims), seq_embed_dim)
        self.task_dense_0 = nn.ModuleDict()
        self.task_dense_1 = nn.ModuleDict()
        self.task_dropout = nn.Dropout(p=0.1)
        self.task_act_1 = nn.LeakyReLU(0.2)
        for i, dim in enumerate(task_type_dims):
            self.task_dense_0[f"task{i}"] = nn.Linear(
                in_features=self.user_concat_dim,
                out_features=self.user_concat_dim // 2
            )
            self.task_dense_1[f"task{i}"] = nn.Linear(
                in_features=self.user_concat_dim // 2,
                out_features=dim
            )

    def split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(len(self.task_type_dims)):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.task_dense_0[f"task{i}"](task_input)
            task_out = self.task_act_1(task_out)
            task_out = self.task_dropout(task_out)
            task_out = self.task_dense_1[f"task{i}"](task_out)
            task_indices.append(task_indice)
            task_outs.append(task_out)
        return task_indices, task_outs

    def forward(self, user_deep_in, page_in, item_in, vl_in, user_wide_in,
                task_type_in=None, search_in=None, sequence_in=None):
        task_type_out = self.task_type_embedding(task_type_in.long())

        if sequence_in:
            sequence_out = []
            for i in range(len(sequence_in)):
                sequence_out.append(self.mm_pooling(self.seq_embedding[i](sequence_in[i].long())))

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        if search_in:
            #        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
            search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
            search_out = self.search_nlp_dense_0(search_out)
            search_out = self.nlp_act(search_out)
            search_out = self.search_nlp_dense_1(search_out)
            search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)

        if search_in:
            if sequence_in:
                user_out = torch.stack([search_out, aep_seq_out, user_ctx_out, task_type_out] + sequence_out, dim=1)
            else:
                user_out = torch.stack([search_out, aep_seq_out, user_ctx_out, task_type_out], dim=1)
        else:
            if sequence_in:
                user_out = torch.stack([aep_seq_out, user_ctx_out, task_type_out] + sequence_out, dim=1)
            else:
                user_out = torch.stack([aep_seq_out, user_ctx_out, task_type_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = torch.concat(user_out.unbind(1), dim=1)
        task_indices, task_outs = self.split_task(task_type_in, user_out)
        return tuple(task_indices), tuple(task_outs), user_aux_loss


    
class GRecUserMultiLabel2(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 page_dim, item_dim, seq_embed_dim, sequence_transformer_kwargs, user_moe_kwargs,
                 task_dim = 140, nlp_dim=0, nlp_encoder_path=None, other_seq_num=None, other_seq_embed_dim=None):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim
        
        self.task_dim = task_dim

        ## user layers
        if other_seq_num:
            self.seq_embedding = nn.ModuleList()
            for i in range(len(other_seq_num)):
                self.seq_embedding.append(nn.Embedding(other_seq_num[i], other_seq_embed_dim[i]))
            # self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
            # self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
            self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        if nlp_dim > 0:
            # self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
            self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
            self.search_nlp_dense_0 = torch.nn.Linear(
                in_features=nlp_dim,
                out_features=seq_embed_dim * 2
            )
            self.search_nlp_dense_1 = torch.nn.Linear(
                in_features=seq_embed_dim * 2,
                out_features=seq_embed_dim
            )
            self.nlp_act = nn.LeakyReLU(0.2)

       # self.user_context_head = ContextTransformerAndWide(
        self.user_context_head = ContextHead(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )

        if nlp_dim > 0:
            if other_seq_num:
                # task_type_out + nlp_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + len(
                    other_seq_num) * seq_embed_dim
            else:
                # task_type_out + nlp_out + aep_seq_out + user_ctx_out
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim
        else:
            if other_seq_num:
                # task_type_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.user_concat_dim = seq_embed_dim + seq_embed_dim + len(other_seq_num) * seq_embed_dim
            else:
                # task_type_out + aep_seq_out + user_ctx_out
                self.user_concat_dim =  seq_embed_dim + seq_embed_dim

        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )
            
        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=self.user_concat_dim//2
        )
        self.user_dense_1 = nn.Linear(
            in_features=self.user_concat_dim//2,
            out_features=self.task_dim
        )


    def forward(self, user_deep_in, page_in, item_in, vl_in, user_wide_in,
                search_in=None, sequence_in=None):
#        task_type_out = self.task_type_embedding(task_type_in.long())

        if sequence_in:
            sequence_out = []
            for i in range(len(sequence_in)):
                sequence_out.append(self.mm_pooling(self.seq_embedding[i](sequence_in[i].long())))

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        if search_in:
            #        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
            search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
            search_out = self.search_nlp_dense_0(search_out)
            search_out = self.nlp_act(search_out)
            search_out = self.search_nlp_dense_1(search_out)
            search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)

        if search_in:
            if sequence_in:
                user_out = torch.stack([search_out, aep_seq_out, user_ctx_out] + sequence_out, dim=1)
            else:
                user_out = torch.stack([search_out, aep_seq_out, user_ctx_out], dim=1)
        else:
            if sequence_in:
                user_out = torch.stack([aep_seq_out, user_ctx_out] + sequence_out, dim=1)
            else:
                user_out = torch.stack([aep_seq_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = torch.concat(user_out.unbind(1), dim=1)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)
        
        return user_out, user_aux_loss

class GRecEPP(nn.Module):
    def __init__(self, offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 page_dim, item_dim, seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        # self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim

        self.user_act = nn.LeakyReLU(0.2)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=seq_embed_dim
        )

        # offer layers
        self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )
        # offer_context_out
        self.offer_concat_dim = seq_embed_dim
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)
        self.offer_dense_0 = nn.Linear(
            in_features=self.offer_concat_dim,
            out_features=self.offer_concat_dim + self.offer_concat_dim // 2
        )
        self.offer_dense_1 = nn.Linear(
            in_features=self.offer_concat_dim + self.offer_concat_dim // 2,
            out_features=seq_embed_dim
        )

        self.out_act = nn.Sigmoid()

    def forward(self, offer_deep_in, page_in, item_in, vl_in, offer_wide_in, search_in):
        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_out = torch.stack([search_out, aep_seq_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = offer_ctx_out
        offer_out = self.offer_dense_0(offer_out)
        offer_out = self.offer_act(offer_out)
        offer_out = self.offer_dropout(offer_out)
        offer_out = self.offer_dense_1(offer_out)
        offer_out = self.offer_act(offer_out)

        out = torch.mul(user_out, offer_out)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out, offer_out


class GRecMultiClass(nn.Module):
    def __init__(self, deep_dims, deep_embed_dims, num_wide, wad_embed_dim, out_dim,
                 page_dim, item_dim, seq_embed_dim, sequence_transformer_kwargs, moe_kwargs,
                 nlp_dim=0, nlp_encoder_path=None, other_seq_num=None, other_seq_embed_dim=None):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        ## user layers
        if other_seq_num:
            self.seq_embedding = dict()
            for i in range(len(other_seq_num)):
                self.seq_embedding[i] = nn.Embedding(other_seq_num[i], other_seq_embed_dim[i] )
            #self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
            #self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
            self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        if nlp_dim > 0:
            #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
            self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
            self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
            )
            self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
            )
            self.nlp_act = nn.LeakyReLU(0.2)

        self.context_head = ContextTransformerAndWide(
            deep_dims=deep_dims,
            num_wide=num_wide,
            deep_embed_dims=deep_embed_dims,
            wad_embed_dim=wad_embed_dim,
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        
        if nlp_dim > 0:
            if other_seq_num:
                # nlp_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + len(self.seq_embedding) * seq_embed_dim
            else:
                # nlp_out + aep_seq_out + user_ctx_out 
                self.concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim 
        else:
            if other_seq_num:
                # aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.concat_dim = seq_embed_dim + seq_embed_dim + len(self.seq_embedding) * seq_embed_dim
            else:
                # aep_seq_out + user_ctx_out 
                self.concat_dim = seq_embed_dim + seq_embed_dim 
        
        
        self.moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=moe_kwargs.get("num_experts"),
            expert_capacity=moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=moe_kwargs.get("num_K"),
        )

        self.act = nn.LeakyReLU(0.2)
        self.dropout = nn.Dropout(p=0.1)
        self.dense_0 = nn.Linear(
            in_features=self.concat_dim,
            out_features=seq_embed_dim * 3
        )
        self.dense_1 = nn.Linear(
            in_features=seq_embed_dim * 3,
            out_features=seq_embed_dim
        )

        self.dense_out = nn.Linear(
            in_features=seq_embed_dim,
            out_features=out_dim
        )

        self.seq_out = {}

    def forward(self, deep_in, page_in, item_in, vl_in, wide_in, 
                search_in = None, 
                sequence_in = None):
        
        device = vl_in.device
        
        if sequence_in:
            sequence_out = []
            for i in range(len(sequence_in)):
                self.seq_embedding[i] = self.seq_embedding[i].to(device)
                sequence_out.append(self.mm_pooling(self.seq_embedding[i](sequence_in[i].long())))
        
        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        if search_in:
            search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
            search_out = self.search_nlp_dense_0(search_out)
            search_out = self.nlp_act(search_out)
            search_out = self.search_nlp_dense_1(search_out)
            search_out = self.nlp_act(search_out)

        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in)
        
        if search_in:
            if sequence_in:
                out = torch.stack([search_out, aep_seq_out, ctx_out] + sequence_out, dim=1)
            else:
                out = torch.stack([search_out, aep_seq_out, ctx_out], dim=1)
        else:
            if sequence_in:
                out = torch.stack([aep_seq_out, ctx_out] + sequence_out, dim=1)
            else:
                out = torch.stack([aep_seq_out, ctx_out] , dim=1)
        out = self.att_pooling(out)
        out, aux_loss = self.moe(out)
        out = out.reshape(-1, self.concat_dim)
        out = self.dense_0(out)
        out = self.act(out)
        out = self.dropout(out)
        out = self.dense_1(out)
        out = self.act(out)
        out = self.dense_out(out)
        out = self.act(out)
        
        return out, aux_loss        
        
class GRecMMOE(nn.Module):
    def __init__(self, deep_dims, deep_embed_dims, num_wide, wad_embed_dim,
                 page_dim, item_dim, seq_embed_dim, sequence_transformer_kwargs, task_dims,
                 nlp_dim=0, nlp_encoder_path=None, other_seq_num=None, other_seq_embed_dim=None, mmoe_kwargs=None):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        ## user layers
        if other_seq_num:
            self.seq_embedding = dict()
            for i in range(len(other_seq_num)):
                self.seq_embedding[i] = nn.Embedding(other_seq_num[i], other_seq_embed_dim[i] )
            #self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
            #self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
            self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        if nlp_dim > 0:
            #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
            self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
            self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
            )
            self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
            )
            self.nlp_act = nn.LeakyReLU(0.2)

        self.context_head = ContextTransformerAndWide(
            deep_dims=deep_dims,
            num_wide=num_wide,
            deep_embed_dims=deep_embed_dims,
            wad_embed_dim=wad_embed_dim,
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        
        if nlp_dim > 0:
            if other_seq_num:
                # nlp_out + aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim + len(self.seq_embedding) * seq_embed_dim
            else:
                # nlp_out + aep_seq_out + user_ctx_out 
                self.concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim 
        else:
            if other_seq_num:
                # aep_seq_out + user_ctx_out + sequence_out_0 + sequence_out_1 + ... + sequence_out_i
                self.concat_dim = seq_embed_dim + seq_embed_dim + len(self.seq_embedding) * seq_embed_dim
            else:
                # aep_seq_out + user_ctx_out 
                self.concat_dim = seq_embed_dim + seq_embed_dim 
        
        
        self.mmoe = MMoE(
            input_size=self.concat_dim,
            expert_hidden_sizes=[
                self.concat_dim,
                self.concat_dim // 2
            ],
#             task_hidden_sizes=[
#                 [task_1_dim],
#                 [task_2_dim]
#             ],
            task_hidden_sizes=[[x] for x in task_dims],
            **mmoe_kwargs
        )
        
#        self.act = nn.LeakyReLU(0.2)
#        self.dropout = nn.Dropout(p=0.1)
#         self.dense_0 = nn.Linear(
#             in_features=self.concat_dim,
#             out_features=seq_embed_dim * 3
#         )
#         self.dense_1 = nn.Linear(
#             in_features=seq_embed_dim * 3,
#             out_features=seq_embed_dim
#         )

#         self.dense_out = nn.Linear(
#             in_features=seq_embed_dim,
#             out_features=out_dim
#         )

        self.seq_out = {}

    def forward(self, deep_in, page_in, item_in, vl_in, wide_in, 
                search_in = None, 
                sequence_in = None):
        
        device = vl_in.device
        
        if sequence_in:
            sequence_out = []
            for i in range(len(sequence_in)):
                self.seq_embedding[i] = self.seq_embedding[i].to(device)
                sequence_out.append(self.mm_pooling(self.seq_embedding[i](sequence_in[i].long())))
        
        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        if search_in:
            search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
            search_out = self.search_nlp_dense_0(search_out)
            search_out = self.nlp_act(search_out)
            search_out = self.search_nlp_dense_1(search_out)
            search_out = self.nlp_act(search_out)

        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in)
        
        if search_in:
            if sequence_in:
                out = torch.cat([search_out, aep_seq_out, ctx_out] + sequence_out, dim=1)
            else:
                out = torch.cat([search_out, aep_seq_out, ctx_out], dim=1)
        else:
            if sequence_in:
                out = torch.cat([aep_seq_out, ctx_out] + sequence_out, dim=1)
            else:
                out = torch.cat([aep_seq_out, ctx_out] , dim=1)
                
#        task1_out, task2_out = self.mmoe(out)
#         print('search_out', search_out.shape)
#         print('aep', aep_seq_out.shape)
#         print('ctx', ctx_out.shape)
#         print('sequence', sequence_out[0].shape)
#         print('concat_dim', self.concat_dim)
#         print('out', out.shape)
        task_outs = self.mmoe(out)
#        return task1_out, task2_out    
        return task_outs
