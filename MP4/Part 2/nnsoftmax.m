function soft = nnsoftmax(z)

norm = sum(exp(z),2);

soft = exp(z) ./ repmat(norm,1,size(z,2));

end 