# Original analysis and geometry; appearance parameters are in layout.R.
invisible(NULL)
library(tidyverse)
library(clusterProfiler)
gene <- data.table::fread("TF_gene.csv", header = T, data.table = F)
gene[1:10, 1:2]
gene <- gene %>% dplyr::filter(source == "NFKB")
gene <- gene$target
gene = bitr(gene, "SYMBOL", "ENTREZID", OrgDb = "org.Hs.eg.db")
gene <- gene$ENTREZID
ego <- enrichGO(gene, OrgDb = "org.Hs.eg.db", qvalueCutoff = 0.05, pvalueCutoff = 0.05, ont = "ALL")
symboldata <- setReadable(ego, OrgDb = "org.Hs.eg.db", keyType = "ENTREZID")
symboldata <- as.data.frame(symboldata)
df <- symboldata %>% group_by(ONTOLOGY) %>% arrange(pvalue) %>% slice_head(n = 5) %>% group_by(ONTOLOGY)
data <- data.frame(ego)
go_MF <- data[data$ONTOLOGY == "MF", ] %>% arrange(p.adjust) %>% .[1:5, ]
go_CC <- data[data$ONTOLOGY == "CC", ] %>% arrange(p.adjust) %>% .[1:5, ]
go_BP <- data[data$ONTOLOGY == "BP", ] %>% arrange(p.adjust) %>% .[1:5, ]
go_enrich_df <- data.frame(ID = c(go_BP$ID, go_CC$ID, go_MF$ID), Description = c(go_BP$Description, go_CC$Description, 
    go_MF$Description), GeneNumber = c(go_BP$Count, go_CC$Count, go_MF$Count), logP = c(-log(go_BP$p.adjust), -log(go_CC$p.adjust), 
    -log(go_MF$p.adjust)), type = factor(c(rep("biological process", 5), rep("cellular component", 5), rep("molecular function", 
    5)), levels = c("molecular function", "cellular component", "biological process"))) %>% group_by(type) %>% 
    arrange_at("logP", .by_group = T)
GO_term_order = factor(as.integer(rownames(go_enrich_df)), labels = go_enrich_df$Description)
library(ggsci)
ggplot(data = go_enrich_df, aes(x = GO_term_order, y = logP, fill = type)) + geom_bar(stat = "identity", width = 0.8) + 
    scale_fill_lancet(alpha = 0.7) + coord_flip() + scale_x_discrete(labels = function(x) str_wrap(go_enrich_df$Description, 
    width = 60)) + scale_y_continuous(expand = c(0, 0)) + labs(y = "-log10Padj", x = NULL) + theme(panel.background = element_blank(), 
    axis.text.x = element_text(face = "bold", size = font_pt, family = "Arial"), axis.text.y = element_text(face = "bold", 
        size = font_pt, family = "Arial"), axis.title.x = element_text(face = "bold", size = font_pt, family = "Arial"), 
    axis.title.y = element_text(face = "bold", size = font_pt, family = "Arial"), plot.title = element_text(size = font_pt, 
        hjust = 0.3, family = "Arial"), legend.position = "right", legend.text = element_text(size = font_pt, family = "Arial"), 
    legend.title = element_text(size = font_pt, family = "Arial"), legend.background = element_rect(fill = "transparent"))
invisible(NULL)
