args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("Usage: Rscript process.R train_file test_file\n")
}

train_data <- read.csv(args[1])     
test_data <- read.csv(args[2])   

X_train <- as.matrix(train_data[, 1])
X_test <- as.matrix(test_data[, 1])


y_train <- train_data[, 2]
y_test <- test_data[, 2]


min_cost <- Inf
best_degree <- -1


for (degree in 1:10) {
  
  X_train_degree <- poly(X_train, degree, raw = TRUE)
  X_test_degree <- poly(X_test, degree, raw = TRUE)
  
  lm_model <- lm(y_train ~ X_train_degree)
  
  cost <- sum((y_test - predict(lm_model, X_test_degree))^2)
  
  if (cost < min_cost) {
    min_cost <- cost
    best_degree <- degree
  }
}

write.table(best_degree, file = paste(sep="", args[1], "_result"), row.names = FALSE, col.names = FALSE)
