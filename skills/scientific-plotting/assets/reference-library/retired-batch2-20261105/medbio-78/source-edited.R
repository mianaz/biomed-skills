library(tidyverse)
library(ggplot2)
library(RColorBrewer)
load(file = "SRA_KEGG_up.Rdata")
symboldata <- data.frame(EGG)
data <- na.omit(symboldata)
ggplot(data, aes(y = Description, x = Count)) + geom_col(aes(fill = category), width = 0.1) + geom_point(aes(size = Count, 
    color = -log10(pvalue)), shape = 16) + scale_size_continuous(range = c(4, 8)) + scale_fill_manual(values = brewer.pal(8, 
    "Set2")) + scale_color_gradientn(colors = colorRampPalette(c("#008bd0", "white", "#ffa61d"))(100), name = "-log10(pvalue)") + 
    scale_x_continuous(expand = c(0, 0), limits = c(0, 12)) + labs(x = "Count", y = NULL, size = "Count") + theme(panel.background = element_blank(), 
    panel.grid = element_blank(), panel.border = element_blank(), axis.text = element_text(color = "black", size = font_pt, 
        family = "Arial"), axis.text.y = element_text(color = "black", size = font_pt, family = "Arial"), axis.title = element_text(size = font_pt, 
        family = "Arial"), axis.title.x = element_text(color = "black", size = font_pt, family = "Arial"), axis.line = element_line(color = "black"), 
    plot.title = element_text(hjust = 1, color = "black", size = font_pt, family = "Arial"), legend.frame = element_rect(colour = "black"), 
    legend.ticks = element_line(colour = "black", linewidth = 0), legend.key.height = unit(0.6, "cm"), legend.title = element_text(color = "black", 
        size = font_pt, family = "Arial"), legend.text = element_text(size = font_pt, family = "Arial")) + guides(color = guide_colorbar(order = 1), 
    size = guide_legend(order = 2)) + scale_y_discrete(labels = function(y) str_wrap(y, width = 40))
invisible(NULL)
