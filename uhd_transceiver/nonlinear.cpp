#include <Eigen/Dense>
#include <fstream>
#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <complex>
#include "wavetable.hpp"

using namespace std;
using namespace Eigen;

MatrixXf x2A(VectorXf & x, int l, int k, int dim)     //A(0,0) is x(0), 1st y is y(k)
{
	int n = l - 1;				// l: length of [x0,...,xn]
	int st = k;					// start of y, x.size() should >= n + 2k, better =
	//int dim = 4;				// dimension of nonlinearity
	
	MatrixXf A(n + 1, 2*k*dim);
	for(int i = 0; i < n + 1; i ++)
	for(int j = 0; j < 2*k; j ++)
	for(int p = 0; p < dim; p ++) 
		A(i, j*dim + p) = pow(x(st - k + j + i),p + 1);		// x^(p + 1) Guy: st-k is always 0 ????  see line -> int st = k;
			//Guy: i=0, j=0,    p[0,dim-1] ->  A(0,0)=x(0)^1,               A(0,1)=x(0)^2, ................... , A(0,dim-1)=x(0)^[dim]
			//Guy: i=0, j=1,    p[0,dim-1] ->  A(0,dim)=x(1)^1,             A(0,dim+1)=x(1)^2, ............... , A(0,2*dim-1)=x(1)^[dim]
			//...
			//Guy: i=0, j=2k-1, p[0,dim-1] ->  A(0,[2k-1]*dim)=x(2k-1)^1,   A(0,[2k-1]*dim+1)=x(2k-1)^2, ..... , A(0,2k*dim-1)=x(2k-1)^[dim]
			//Guy: new row                   _____________________________________________________________________________________________
			//Guy: i=1, j=0,    p[0,dim-1] ->  A(1,0)=x(1)^1,               A(1,1)=x(1)^2, ................... , A(1,dim-1)=x(1)^[dim]
			//Guy: i=1, j=1,    p[0,dim-1] ->  A(1,dim)=x(2)^1,             A(1,dim+1)=x(2)^2, ............... , A(1,2*dim-1)=x(2)^[dim]
			//...
			//Guy: i=1, j=2k-1, p[0,dim-1] ->  A(1,[2k-1]*dim)=x(2k)^1,     A(1,[2k-1]*dim+1)=x(2k)^2, ....... , A(1,2k*dim-1)=x(2k)^[dim]
			//Guy: new row                   _____________________________________________________________________________________________
			//                               .............................................................................................
			//                               .............................................................................................
			//Guy: new row                   _____________________________________________________________________________________________
			//Guy: i=n, j=0,    p[0,dim-1] ->  A(n,0)=x(n)^1,               A(n,1)=x(n)^2, ................... , A(n,dim-1)=x(n)^[dim]
			//Guy: i=n, j=1,    p[0,dim-1] ->  A(n,dim)=x(n+1)^1,           A(n,dim+1)=x(n+1)^2, ............. , A(n,2*dim-1)=x(n+1)^[dim]
			//...
			//Guy: i=n, j=2k-1, p[0,dim-1] ->  A(n,[2k-1]*dim)=x(2k-1+n)^1, A(n,[2k-1]*dim+1)=x(2k-1+n)^2, ... , A(n,2k*dim-1)=x(2k-1+n)^[dim]
	return A;
}

MatrixXf x2A(VectorXf & x, int k, int dim)
{
	int lx = x.size();
	return x2A(x, lx - 2*k + 1, k, dim);
}

MatrixXf x2A(VectorXf & x, int k)	        // default dim is 1
{
	return x2A(x, k, 1);
}

/*
 // record linear cancellation for back up
MatrixXf x2A(VectorXf& x, int l, int k)		// Note A(0,0) is x(0), so the 1st y is y(k)
{
	int n = l - 1;							// l is the length of [x0, x1, ..., xn]
	int st = k;								// normally x.size() should not be less than n + 2k
	MatrixXf A(n + 1, 2*k);					// should be check a third time!
	for(int i = 0; i < n + 1; i++)
	for(int j = 0; j < 2*k; j++)
	{
		A(i,j) = x(st - k + j + i);
 	}
	return A;
}

MatrixXf x2A(VectorXf& x, int k)
{
	int lx = x.size();	
	MatrixXf A = x2A(x, lx - 2*k + 1, k);			   // every points are used
	return A;
}*/