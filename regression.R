args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("Usage: Rscript process.R train_file test_file\n")
}


min_cost <- Inf
best_degree <- -1

for (degree in 1:10) {
  cost <- sum((read.csv(args[2])[, 4] - predict(lm(read.csv(args[1])[, 4] ~ poly(as.matrix( read.csv(args[1])[, 3]), degree, raw = TRUE)), poly(as.matrix(read.csv(args[2])[, 3]), degree, raw = TRUE)))^2)

  if (cost < min_cost) {
    min_cost <- cost
    best_degree <- degree
  }
}

write.table(best_degree, file = paste(sep="", args[1], "_result"), row.names = FALSE, col.names = FALSE)
