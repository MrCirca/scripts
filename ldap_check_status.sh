#!/bin/bash
BASE_DN=$1
PROVIDER_URI=$2
LDAP_CSN_CONSUMER_COMMAND=$(ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -s base -b "$BASE_DN" contextCSN 2>&1)
LDAP_CSN_CONSUMER_RC=$?
LDAP_CSN_PROVIDER_COMMAND=$(ldapsearch -LLL -x -H ldaps://"$PROVIDER_URI" -s base -b "$BASE_DN" contextCSN 2>&1)
LDAP_CSN_PROVIDER_RC=$?
PROVIDER_CSN=$(echo -e $LDAP_CSN_PROVIDER_COMMAND | grep contextCSN | cut -d " " -f 2)
CONSUMER_CSN=$(echo -e $LDAP_CSN_CONSUMER_COMMAND | grep contextCSN | cut -d " " -f 2)

if [[ "$LDAP_CSN_CONSUMER_RC" != "0" ]] && [[ "$LDAP_CSN_PROVIDER_RC" == "0" ]]; then
 	echo "1"

elif [[ "$LDAP_CSN_PROVIDER_RC" != "0" ]] && [[ "$LDAP_CSN_CONSUMER_RC" == "0" ]]; then
	echo "2"

elif [[ "$LDAP_CSN_PROVIDER_RC" != "0" ]] && [[ "$LDAP_CSN_CONSUMER_RC" != "0"  ]]; then
	echo "3"

elif [[ "$PROVIDER_CSN" == "$CONSUMER_CSN" ]]; then
	echo "4"
else
	echo "100"
fi
