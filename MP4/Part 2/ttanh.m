function g = ttanh(z)
g = (exp(z) - exp(-z)) ./ (exp(z) + exp(-z));
end
