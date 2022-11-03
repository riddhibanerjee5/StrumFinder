#include <iostream>
#include <fstream>
#include <complex>
#include <vector>
using namespace std;

#define PI 3.14159265358979323846

vector<complex<double>> computeDft(const vector<double>& input) {
	vector<complex<double> > output;
	size_t n = input.size();
	for (size_t k = 0; k < n; k++) {  // For each output element
		complex<double> sum(0, 0);
		for (size_t t = 0; t < n; t++) {  // For each input element
			double angle = 2 * PI * t * k / n;
			sum += input[t] * exp(complex<double>(0, -angle));
		}
		output.push_back(sum);
	}
	return output;
}

vector<vector<complex<double>>> stft(vector<double>& n, vector<double>& t, vector<double>& w, vector<double> x, int W, double Fs)
{
	int M = floor(x.size() / W);
	vector<vector<complex<double>>> X;
	X.reserve(M);
	n.reserve(M);
	t.reserve(M);
	w.reserve(W);

	for (int i = 0; i < M; i++)
	{
		n.push_back(i * W);
		t.push_back(n[i] / Fs);
		vector<double> y = vector<double>(x.begin() + (i * W), x.begin() + ((i + 1) * W));
		X.push_back(computeDft(y));
	}
	for (int i = 0; i < W; i++)
		w.push_back((2.0 * PI * i) / double(W));

	return X;
}

int main()
{
	/*// chirp sound
	ifstream file;
	file.open("chirp.txt");
	string val;
	vector<double> x;
	int W = 100; // length of segments to take fourier transform of
	if (file.is_open())
	{
		while (getline(file, val))
			x.push_back(stod(val));
	}
	else
		cout << "Unable to open file" << endl;
	*/
	// custom vector
	vector<double> x = { 0.00, 0.59, 0.95, 0.95, 0.59, 0.00, -0.59, -0.95, -0.95, -0.59, 0.00, 0.95, 0.59, -0.59, -0.95, 0.00, 0.95, 0.59, -0.59, -0.95, 0.00, 0.95, -0.59, -0.59, 0.95, 0.00, -0.95, 0.59, 0.59, -0.95, 0.00, 0.59, -0.95, 0.95, -0.59, 0.00, 0.59, -0.95, 0.95, -0.59, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.59, 0.95, -0.95, 0.59, 0.00, -0.59, 0.95, -0.95, 0.59, 0.00, -0.95, 0.59, 0.59, -0.95, 0.00, 0.95, -0.59, -0.59, 0.95, 0.00, -0.95, -0.59, 0.59, 0.95, 0.00, -0.95, -0.59, 0.59, 0.95, 0.00, -0.59, -0.95, -0.95, -0.59, 0.00, 0.59, 0.95, 0.95, 0.59, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00 };
	int W = 34; // length of segments to take fourier transform of
	
	double Fs = 44100.0; // sampling rate (CD)
	vector<double> n, t, w; // sample, frequency, and time vectors
	vector<vector<complex<double>>> X = stft(n, t, w, x, W, Fs);
	cout << "SHORT TIME FOURIER TRANSFORM (complex numbers)" << endl;
	for (unsigned int i = 0; i < X.size(); i++)
	{
		for (unsigned int j = 0; j < X[i].size(); j++)
		{
			if (abs(X[i][j]) < 0.0000001)
				X[i][j] = 0.0;
			cout << "X[" << i << "][" << j << "]: " << X[i][j] << endl;
		}
	}
	cout << "\nFREQUENCIES" << endl;
	for (int i = 0; i < W; i++)
	{
		cout << "w[" << i << "]: " << w[i] << endl;
	}
	return 0;
}