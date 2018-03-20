struct address;
struct degreeType;
struct revokingOrder{
	rawTransaction;
}

struct certificate{
	rawTransaction;
	univerityPublicKey;
	degreeType;
	student;
}
struct student{
	publicKey;
	identity;
};

struct university{
	address;
	name;
};

struct proof{
	transactionID;
};

// singleton
struct highAuthority 
{
	publicKey;
	name;
};


int runChain (name)
{
	return errorCode;
}

address setBurnAddress (void);

int activateUniversity (university)
{
	return errorCode;
}

int giveIssuePermission (university, degreeType);
list<degreeType> listIssuePermissions (university);

int revokeIssuePermission (university, degreeType)
{
	return errorCode;
}

int revokeUniversity (university)
{
	return errorCode;
}

int saveUniversity (university)
{
	return errorCode;
}
university loadUniversity (name);
int approveRevokingOrder (revokingOrder)
{
	// signs transaction and publishes it
}

//-------------------------------

int acceptStudent (student)
{
	// grant send, receive
}

certificate issueCertificate (degreeType, student, university, highAuthority)
{
	// returns an unsigned transaction from SU multisig to SUH multisig.
}

certificate signCertificate (certificate);

proof publishCertificate (certificate);
revokingOrder revokeCertificate (degreeType, student, university, highAuthority)
{
	// returns a raw transaction from SUH multisig to burnaddress;
}


int saveStudent (student);
student loadStudent (identity);



//---------------------------------
certificate signCertificate (certificate)
{
	// generates SU multisig and signs the certificate
}

bool validateCertificate (proof);


