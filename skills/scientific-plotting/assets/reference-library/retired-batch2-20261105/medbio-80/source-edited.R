# Original analysis and geometry; appearance parameters are in layout.R.
invisible(NULL)
library(tidyverse)
library(ggplot2)
library(ggrepel)
library(RColorBrewer)
library(clusterProfiler)
load(file = "GSE7621_allDiff.Rdata")
gene = rownames(allDiff)
gene = bitr(gene, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = "org.Hs.eg.db")
gene <- dplyr::distinct(gene, SYMBOL, .keep_all = T)
gene_df <- data.frame(logFC = allDiff$logFC, SYMBOL = rownames(allDiff))
gene_df <- merge(gene_df, gene, by = "SYMBOL")
genelist <- gene_df$logFC
names(genelist) <- gene_df$SYMBOL
genelist <- sort(genelist, decreasing = T)
head(genelist)
hallmarks <- read.gmt("h.all.v2023.2.Hs.symbols_modify.gmt")
gsearesult <- GSEA(genelist, TERM2GENE = hallmarks, pvalueCutoff = 1, minGSSize = 1, maxGSSize = 5e+05)
data <- gsearesult[, c("ID", "NES", "setSize", "pvalue")]
data$setSize <- data$setSize/10
data <- data[order(data$NES, decreasing = T), ]
data$ID <- factor(data$ID, levels = data$ID)
data$xlab <- 1:50
label <- c("TNFA SIGNALING VIA NFKB", "IL6 JAK STAT3 SIGNALING", "INFLAMMATORY RESPONSE", "INTERFERON GAMMA RESPONSE", 
    "HYPOXIA", "ANGIOGENESIS", "G2M CHECKPOINT", "E2F TARGETS", "FATTY ACID METABOLISM", "OXIDATIVE PHOSPHORYLATION")
data_label <- data[data$ID %in% label, ]
data_label$color <- c("#E31A1C", "#FB9A99", "#FF7F00", "#6A3D9A", "#33A02C", "black", "black", "black", "#80B1D3", 
    "#1F78B4")
ggplot(data = data, aes(x = xlab, y = NES)) + geom_point(aes(size = setSize, alpha = -log10(pvalue)), shape = 21, 
    stroke = 0.8, fill = "#1F78B4", color = "black") + scale_size_continuous(range = c(1, 8)) + scale_x_continuous(breaks = seq(0, 
    50, 10), labels = seq(0, 50, 10)) + scale_y_continuous(breaks = seq(-4, 3, 1), labels = seq(-4, 3, 1)) + theme(axis.line = element_line(color = "black"), 
    axis.text = element_text(color = "black", size = font_pt, family = "Arial"), axis.title = element_text(color = "black", 
        size = font_pt, family = "Arial"), plot.title = element_text(color = "black", size = font_pt, hjust = 0.5, 
        family = "Arial"), legend.title = element_text(color = "black", size = font_pt, family = "Arial"), legend.text = element_text(color = "black", 
        size = font_pt, family = "Arial"), panel.grid = element_blank(), panel.background = element_blank()) + 
    labs(x = "Hallmark genesets", y = "Normalized enrichment score", title = "GSE7621 GSEA Hallmark Enrichment") + 
    guides(size = guide_legend(title = "Detection\n(proportion)", order = 2), alpha = guide_legend(title = "Significance\n(-log10pvalue)", 
        order = 1)) + geom_text_repel(data = data_label, aes(x = xlab, y = NES, label = ID), size = font_pt/ggplot2::.pt, 
    color = data_label$color, force = 10, min.segment.length = 0, hjust = 1.5, box.padding = 0.5, segment.color = "grey20", 
    segment.size = 0.3, family = "Arial")
invisible(NULL)
