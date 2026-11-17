# Import KEGG layout and relations for a reviewed mechanism scene.
# Rscript pathway_layout.R pathway.xml pathway-layout.json
library(xml2)
library(jsonlite)
suppressPackageStartupMessages(library(pathview))
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("Supply a KGML file and an output JSON path.")
kgml <- read_xml(args[1])
info <- node.info(args[1])
pathway_id <- sub("^path:", "", xml_attr(kgml, "name"))
nodes <- lapply(names(info$type), function(id) list(
  id = paste(pathway_id, id, sep = ":"), source_entry = id,
  gene_ids = as.list(info$kegg.names[[id]]), label = unname(info$labels[id]),
  type = unname(info$type[id]),
  source_position = list(x = unname(info$x[id]), y = unname(info$y[id]),
                        width = unname(info$width[id]), height = unname(info$height[id]))
))
relations <- lapply(xml_find_all(kgml, ".//relation"), function(e) list(
  from = paste(pathway_id, xml_attr(e, "entry1"), sep = ":"),
  to = paste(pathway_id, xml_attr(e, "entry2"), sep = ":"),
  type = xml_attr(e, "type"),
  subtypes = lapply(xml_find_all(e, "subtype"), function(s) list(
    name = xml_attr(s, "name"), value = xml_attr(s, "value")))
))
groups <- lapply(xml_find_all(kgml, ".//entry[@type='group']"), function(e) list(
  id = paste(pathway_id, xml_attr(e, "id"), sep = ":"),
  members = as.list(paste(pathway_id, xml_attr(xml_find_all(e, "component"), "id"), sep = ":"))
))
reactions <- lapply(xml_find_all(kgml, ".//reaction"), function(e) list(
  entry = xml_attr(e, "id"), name = xml_attr(e, "name"), type = xml_attr(e, "type"),
  substrates = as.list(xml_attr(xml_find_all(e, "substrate"), "id")),
  products = as.list(xml_attr(xml_find_all(e, "product"), "id"))
))
result <- list(schema = "biomed-pathway-layout/1", pathway = pathway_id,
  title = xml_attr(kgml, "title"), species = xml_attr(kgml, "org"),
  source = list(format = "KEGG KGML", file = basename(args[1]), url = xml_attr(kgml, "link"),
    parser = paste0("pathview::node.info ", packageVersion("pathview"))),
  nodes = nodes, groups = groups, relations = relations, reactions = reactions,
  layout_role = "Starting positions and branch order; mechanism events and compartment placement are reviewed separately.")
write_json(result, args[2], pretty = TRUE, auto_unbox = TRUE, null = "null")
cat(length(nodes), "nodes,", length(groups), "groups,", length(relations), "relations\n")
