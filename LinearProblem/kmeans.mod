// Number of observations
int m = ...;
// Number of variables per observation
int n = ...;
// Number of Classes
int k = ...;

// Range variables
range M = 1..m;
range N = 1..n;

// Input matrix A with all data used in the clustering
float A[M][N] = ...;
// Matrix with the euclidian distance between every two observations in A
float D[M][M];

// Decision boolean variable telling if observation 'i' is in cluster 'j'
dvar boolean X[M][M];

// Calculating the matrix with the euclidian distances D
execute {
	for (var i=1;i<=m;i++) {
		for (var j=1;j<=m;j++){
		    var sum2 = 0;
			for (var l=1;l<=n;l++) {
   				sum2 = sum2 + Math.pow((A[i][l]-A[j][l]), 2);
			}
			D[i][j] = Math.pow(sum2, 0.5);
		}
	}	  
}

// Objective function is to minimize the summation of the euclidian distances ... 
// ... of each observation to the assigned cluster. 
// Divided by 2, once each distance is computed twice: [i][j] and [j][i]
minimize 
sum(i in M)
	(sum(j in M) 
		(D[i][j]*X[i][j])/2);

subject to {
	// Constraint 1: Each observation must be assigned to only 1 cluster
    forall (i in M)
      sum(j in M) X[i][j] == 1;
    // Constraint 2: There must be k clusters
    sum(j in M) X[j][j] == k;
    // Constraint 3: An observation can belong to a cluster only if the cluster exists
    forall (i in M, j in M) 
	  X[j][j] >= X[i][j];
	// Same as Constraint 3 but slower (49:65 vs 2:20)
//	forall (j in M) 
//	  m*X[j][j] >= sum (i in M) X[i][j];
	  
}

// Printing the results considering the element and its assigned cluster
execute {
 	writeln("Element, Class");
    for (var i in M) {
	  	for (var j in M) {
	  	    if (X[i][j] == 1) {
	  	      writeln(i + "," + j);
	  	    }
	    }
    }
} 
