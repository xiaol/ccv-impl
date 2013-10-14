//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h> // mac os x

//#include <malloc.h>

#include <Python/Python.h>

//gcc -fPIC distance-py.c -o distance.so -shared -framework Python

const long long max_size = 2000;         // max length of strings
const long long N = 40;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

/*int main(int argc, char **argv) {
	char *filePath = "../bin/vectors.bin";
	char *words = "健身 养生";
	similar(filePath, words);
	return 0;
}*/


long long words, size;
float *M;
char *vocab;
char bestw[40][2000];

int similar(char* filePath, char* tuple){

	char st1[max_size];
	char  st[100][max_size];
	float dist, len, bestd[N], vec[max_size];
	long long  a, b, c, d, cn, bi[100];



	//strcpy(file_name, filePath);
	//printf("%s",file_name);

	for (a = 0; a < N; a++)
		bestd[a] = 0;
	for (a = 0; a < N; a++)
		bestw[a][0] = 0;
	strcpy(st1, tuple);

	cn = 0;
	b = 0;
	c = 0;
	while (1) {
		st[cn][b] = st1[c];
		b++;
		c++;
		st[cn][b] = 0;
		if (st1[c] == 0)
			break;
		if (st1[c] == ' ') {
			cn++;
			b = 0;
			c++;
		}
	}
	cn++;
	for (a = 0; a < cn; a++) {
		for (b = 0; b < words; b++)
			if (!strcmp(&vocab[b * max_w], st[a]))
				break;
		if (b == words)
			b = -1;
		bi[a] = b;
		printf("\nWord: %s  Position in vocabulary: %lld\n", st[a], bi[a]);
		if (b == -1) {
			printf("Out of dictionary word!\n");
			//break;
		}
	}
	//if (b == -1) continue;
	printf(
			"\n                                              Word       Cosine distance\n------------------------------------------------------------------------\n");
	for (a = 0; a < size; a++)
		vec[a] = 0;
	for (b = 0; b < cn; b++) {
		if (bi[b] == -1)
			continue;
		for (a = 0; a < size; a++)
			vec[a] += M[a + bi[b] * size];
	}
	len = 0;
	for (a = 0; a < size; a++)
		len += vec[a] * vec[a];
	len = sqrt(len);
	for (a = 0; a < size; a++)
		vec[a] /= len;
	for (a = 0; a < N; a++)
		bestd[a] = 0;
	for (a = 0; a < N; a++)
		bestw[a][0] = 0;
	for (c = 0; c < words; c++) {
		a = 0;
		for (b = 0; b < cn; b++)
			if (bi[b] == c)
				a = 1;
		if (a == 1)
			continue;
		dist = 0;
		for (a = 0; a < size; a++)
			dist += vec[a] * M[a + c * size];
		for (a = 0; a < N; a++) {
			if (dist > bestd[a]) {
				for (d = N - 1; d > a; d--) {
					bestd[d] = bestd[d - 1];
					strcpy(bestw[d], bestw[d - 1]);
				}
				bestd[a] = dist;
				strcpy(bestw[a], &vocab[c * max_w]);
				break;
			}
		}
	}
	for (a = 0; a < N; a++)
		printf("%50s\t\t%f\n", bestw[a], bestd[a]);

	return 1;
}

PyObject* wrap_similar(PyObject* self, PyObject* args) {
	char *filePath, *tuple;
	int result;

	if (!PyArg_ParseTuple(args, "ss:similar", &filePath, &tuple))
		return NULL;
	result = similar(filePath, tuple);

	if (result == -1)
		return Py_BuildValue("i", -1);

	PyObject *dict = NULL;
	PyListObject *list;

	list = (PyListObject *) Py_BuildValue("[]");

	int i = 0;
	for (i; i < N; i++) {
		dict = Py_BuildValue("s", bestw[i]);
		PyList_Append(list, dict);
	}
	return (PyObject *) list;

}

static PyMethodDef distanceMethods[] = { { "similar", wrap_similar,
		METH_VARARGS, "Similar Words." }, { NULL, NULL } };

void initdistance() {
	PyObject* m;
	m = Py_InitModule("distance", distanceMethods);

	FILE *f;
	float len;
	long long  a, b;
	char ch;
	char *file_name = "../bin/vectors.bin";
	f = fopen(file_name, "rb");
		if (f == NULL) {
			printf("Input file not found\n");
			return;
		}
		fscanf(f, "%lld", &words);
		fscanf(f, "%lld", &size);
		vocab = (char *) malloc((long long) words * max_w * sizeof(char));
		M = (float *) malloc((long long) words * (long long) size * sizeof(float));
		if (M == NULL) {
			printf("Cannot allocate memory: %lld MB    %lld  %lld\n",
					(long long) words * size * sizeof(float) / 1048576, words,
					size);
			return;
		}
		for (b = 0; b < words; b++) {
			fscanf(f, "%s%c", &vocab[b * max_w], &ch);
			for (a = 0; a < size; a++)
				fread(&M[a + b * size], sizeof(float), 1, f);
			len = 0;
			for (a = 0; a < size; a++)
				len += M[a + b * size] * M[a + b * size];
			len = sqrt(len);
			for (a = 0; a < size; a++)
				M[a + b * size] /= len;
		}
		fclose(f);
}
