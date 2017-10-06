# P400 - Insane in the Blockchain

## Description

Check out this transaction, on the Ethereum blockchain:
https://etherscan.io/address/0x55dfcea405a1c9b7336cd2286c2c3040f9b13e7d

We know [this binary](../blob/master/Pwnable/P400-InsaneInTheBlockChain/bin/geth) was used to sign it.

Extract the private key used to sign this transaction.

## Solution

  * Investigate how [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) works
  * The geth binary is backdoored. Every signature will use k = "four"

### Possible strategy
  * Start the binary
  * Do some transactions and check the resulting signatures. You should notice
that `r` is always the same. This implies that `k` is being reused...
  * Find the value of `k`

### Running the binary
  * Run it on a Raspberry Pi 3
  * Using [this method](https://reverseengineering.stackexchange.com/questions/8829/cross-debugging-for-mips-elf-with-qemu-toolchain)
  * Or [this one](https://wiki.ubuntu.com/ARM/BuildEABIChroot)
  * Or [this one](https://hub.docker.com/r/resin/armv7hf-debian/) Thanks to [morisson](https://twitter.com/morisson) for the suggestion

### Finding k

Two possible approaches

  * Reverse engineer the binary and find out the value of k
    * Fetch the [geth source code](https://github.com/ethereum/go-ethereum/wiki/geth)
    * Find out which function generates k and work from there (using dynamic or static RE)
    * Google "ecdsa k reuse". Use [this tool](https://github.com/tintinweb/ecdsa-private-key-recovery) and plug in known k (no need for two signatures)
      
  * Analytical method
    * Perform two signatures with some key
    * Google "edsa k reuse". Use [this tool](https://github.com/tintinweb/ecdsa-private-key-recovery)
    * Alternatively, having a known key allows us to extract `k` directly. Having `k` allows us to extract the private key from only transaction only. Check out the [solution file](../blob/master/Pwnable/P400-InsaneInTheBlockChain/solution/solution.py)

