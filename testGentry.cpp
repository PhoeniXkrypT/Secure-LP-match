#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h> 
#include <sys/time.h> 

#include "gentryextended.h"
using namespace std;

int main(int argc, char *argv[]) {
  timeval time1, time2, time3, time4, time5, time6, time8, time9;
	long inp_value, value=0;
  mpz_t test_value, encTest, db_value, encDBval, diff, blind_diff, val, rand_value, tmp;
  mpz_inits(test_value, encTest, db_value, encDBval, diff, blind_diff, val, rand_value, tmp, NULL);

  //Cryptosystem parameters 
  int n = 1024;
  int t = 380;
  int zp = 36; // Bit-size of the clear-text

	printf("Entering Encrypted domain : extended Gentry's system\n");
	gettimeofday(&time1,NULL);

  GentryPrivKeys* privKeys;
  GentryPubKeys* pubKeys;

 //Generate keys
  GentryExtended::generateKeys2(n, t, privKeys, pubKeys, false);
  gettimeofday(&time2,NULL);
  GentryExtended* crypto = new GentryExtended(*privKeys, zp, true);

  //The GentryExtended object contains both the public and private keys.
  //In a real setting, only the public keys would be sent to the operator

  delete privKeys;
  delete pubKeys;

  int flag = 0;
  if (argc < 3) 
  {
    printf("Usage: ./main <license-plate-value> <database-file>\n");
    exit(0);
  }

  mpz_set_si(tmp ,0);
  inp_value = atol(argv[1]);
  mpz_set_si(test_value, inp_value);

  gettimeofday(&time3,NULL);
  crypto->Encrypt(encTest, test_value);
  gettimeofday(&time4,NULL);

	ifstream file(argv[2]);
	cout <<"__Checking in Database__"<< std::endl;

  gettimeofday(&time5,NULL);
  while (file>>value)
  {
    mpz_set_si(db_value, value);
    crypto->Encrypt(encDBval, db_value);
    mpz_set_si(rand_value, rand());

    crypto->HomomorphicSub(diff, encTest, encDBval);
    crypto->HomomorphicMul(blind_diff, diff, rand_value);
  gettimeofday(&time8,NULL);
    crypto->Decrypt(val, blind_diff);
  gettimeofday(&time9,NULL);
    if (mpz_cmp(val, tmp) == 0)
      flag = 1;
	}
	gettimeofday(&time6,NULL);

  mpz_clears(test_value, encTest, db_value, encDBval, diff, blind_diff, val, rand_value, tmp, NULL);

  if (flag == 0)
    cout <<"\nMatch Not Found !\n"<< endl;
  else
    cout <<"\nMatch Found !\n"<< endl;

	printf("Time taken for key generation %f secs\n", (double) (time2.tv_usec - time1.tv_usec) / 1000000 +
     (double) (time2.tv_sec - time1.tv_sec));
	printf("Time taken for one encryption %f secs\n", (double) (time4.tv_usec - time3.tv_usec) / 1000000 +
     (double) (time4.tv_sec - time3.tv_sec));
	printf("Time taken for finding match %f secs\n", (double) (time6.tv_usec - time5.tv_usec) / 1000000 +
     (double) (time6.tv_sec - time5.tv_sec));

printf("Time taken for one dec %f secs\n", (double) (time9.tv_usec - time8.tv_usec) / 1000000 +     (double) (time9.tv_sec - time8.tv_sec));
/*	printf(" %f\n", (double) (time6.tv_usec - time5.tv_usec) / 1000000 +
     (double) (time6.tv_sec - time5.tv_sec));*/

  delete crypto;
  return 0;
}

