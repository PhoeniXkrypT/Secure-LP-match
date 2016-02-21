#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <sys/time.h>

//include library headers
#include "core/big_integer.h"
#include "core/paillier.h"

using namespace SeComLib::Core;
using namespace SeComLib::Utils;

int main (int argc, char *argv[]) {
	//it will require a config.xml file in the same directory as the executable
	timeval time1, time2, time3, time4, time5, time6, time8, time9;
	printf("Entering Encrypted domain : Paillier Encryption\n");

  gettimeofday(&time1,NULL);
	Paillier privateCryptoProvider;
	privateCryptoProvider.GenerateKeys();
	gettimeofday(&time2,NULL);

  Paillier publicCryptoProvider(privateCryptoProvider.GetPublicKey());
	long inp_value;
  int flag = 0;
  if (argc < 3)
  {
    printf("Usage: ./main <license-plate-value> <database-file>\n");
    exit(0);
  }

	inp_value = atol(argv[1]);

	BigInteger test_value(inp_value);
	gettimeofday(&time3,NULL);
	Paillier::Ciphertext encTest = publicCryptoProvider.EncryptInteger(test_value);
	gettimeofday(&time4,NULL);

  std::ifstream file(argv[2]);
  std::string str; 
	std::cout <<"__Checking in Database__"<< std::endl;

	gettimeofday(&time5,NULL);
  while (std::getline(file, str))
  {
    BigInteger db_value(str);
    Paillier::Ciphertext encDBval = publicCryptoProvider.EncryptInteger(db_value);
    long rand_value = rand();

    Paillier::Ciphertext diff = encTest - encDBval;
    Paillier::Ciphertext blind_diff = diff * rand_value;
	gettimeofday(&time8,NULL);
    BigInteger val = privateCryptoProvider.DecryptInteger(blind_diff);
	gettimeofday(&time9,NULL);
    if (val == 0)
      flag = 1;
  }
	gettimeofday(&time6,NULL);

  if (flag == 0)
    std::cout <<"\nMatch Not Found !\n"<< std::endl;
  else
    std::cout <<"\nMatch Found !\n"<< std::endl;

	printf("Time taken for key generation %f secs\n", (double) (time2.tv_usec - time1.tv_usec) / 1000000 +
    (double) (time2.tv_sec - time1.tv_sec));
	printf("Time taken for one encryption %f secs\n", (double) (time4.tv_usec - time3.tv_usec) / 1000000 +
     (double) (time4.tv_sec - time3.tv_sec));
	printf("Time taken for finding match %f secs\n", (double) (time6.tv_usec - time5.tv_usec) / 1000000 +
     (double) (time6.tv_sec - time5.tv_sec));
printf("Time taken for one dec %f secs\n", (double) (time9.tv_usec - time8.tv_usec) / 1000000 +     (double) (time9.tv_sec - time8.tv_sec));
/*	printf("%f\n", (double) (time6.tv_usec - time5.tv_usec) / 1000000 +
     (double) (time6.tv_sec - time5.tv_sec));*/

	return 0;
}
