function g = ttanhGradient(z)

g = 1-ttanh(z).*ttanh(z);

end
