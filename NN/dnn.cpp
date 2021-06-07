#include <iostream>
#include <random>
#include <string>
#include <vector>
#include <math>

using namespace std;

int tanh(double &x){
	return 0;
}

int sigmoid(double &x){
	return 1 / (1 + exp(-x));	
}

int main(){

	int num_data = 10;
	int num_dims = 5;
	int num_layers = 3;
	int num_class = 2;

	vector<vector<double>> X(num_data, vector<double>(num_dims));
	vector<int> Y(num_data);
	vector<int> layers = {num_data, 16, 16, num_class}

	vector<vector<double>> W_i1(num_dims, vector<double>(layers[1], 1));
	vector<vector<double>> W_12(layers[1], vector<double>(layers[2],1));
	vector<vector<double>> W_2o(layers[2], vector<double>(num_class,1));

	vector<double> layer1(layers[1]);
	vector<double> layer2(layers[2]);
	vector<double> layer3(layers[3]);

	for(int i = 0; i < num_data; i++){
		for(int j = 0; j < num_dims; j++){
			X[i][j] = rand() % 6 + 1;
		}
		if (accmulate(X[i].begin(), X[i].end(), 0) >= 30)
			Y[i] = 1;
		else
			Y[i] = 0;
	}

	for(int n = 0; n < N; n++){
		// forward pass
		for(int i = 0; i < num_layers-1; i++){
			for(int j = 0; j < layers[i]; j++){
				for(int k = 0; 	k < layers[i+1]; k++){
					if (i == 0){
						layer1[k] += X[n][j] * W_i1[j][k];
					}
					else if (i == 1){
						layer2[k] += layer1[j] * W_12[j][k];
					}
					else if (i == 2){
						layer3[k] += layer2[j] * W_2o[j][k];
					}
				}
			}
			if (i == 0){
				for(int i = 0; i < layer1.size(); i++)
					layer1[i] = sigmoid(layer1[i]);
			}
		
			else if (i == 1){
				for(int i = 0; i < layer2.size(); i++)
					layer2[i] = sigmoid(layer2[i]);
			}

			else if (i == 2){
				for(int i = 0; i < layer3.size(); i++)
					layer3[i] = sigmoid(layer3[i]);
			}
		}
		
		double E = 0;
		vector<int> label(2);
		if (Y[n] == 0)
			label = {1, 0};
		else
			label = {0, 1};
		for(int i = 0; i < layer3.size(); i++){
			E += pow(layer3[i] - label[i], 2);
		}

		cout << "sample: " << n << " Error = " << E << endl;

		//backward pass
		for(int i = num_layers; i > 0; i--){
			for(int j = 0; j < layers[i]; j++){
				for(int k = 0; k < layers[i-1]; k++){
					if (i == 3){
						W_2o[j][k] = W_2o[j][k] - lr * (1-layer3[j]) * layer3[j] * (layer3[j] - label[j]) * layer2[k];
					}
				}
			}
		}
	}
	
	return 0;
}

