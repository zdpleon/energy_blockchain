/*
Copyright IBM Corp. 2016 All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

		 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main


import (
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)

// SimpleChaincode example simple Chaincode implementation
type SimpleChaincode struct {
}

func (t *SimpleChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response  {
        fmt.Println("########### example_cc Init ###########")
	_, args := stub.GetFunctionAndParameters()
	var A, B, C, D, E, P ,F, G string    // Entities
	var Aval, Bval, Cval, Dval, Eval, Pval, Fval,Gval  float64 // Asset holdings
	var err error

	if len(args) != 16 {
		return shim.Error("Incorrect number of arguments. Expecting 16")
	}

	// Initialize the chaincode
	A = args[0]
	Aval, err = strconv.ParseFloat(args[1],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	B = args[2]
	Bval, err = strconv.ParseFloat(args[3],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	C = args[4]
	Cval, err = strconv.ParseFloat(args[5],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	D = args[6]
	Dval, err = strconv.ParseFloat(args[7],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	F = args[8]
	Eval, err = strconv.ParseFloat(args[9],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}	
	G = args[10]
	Eval, err = strconv.ParseFloat(args[11],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	E = args[12]
	Eval, err = strconv.ParseFloat(args[13],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	P = args[14]
	Eval, err = strconv.ParseFloat(args[15],64)
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}	
	
	fmt.Printf("Aval = %0.2f, Bval = %0.2f, Cval = %0.2f, Dval = %0.2f, Fval = %0.2f , Gval = %0.2f, Electricity = %0.2f, Price = %0.2f\n", Aval, Bval, Cval, Dval, Fval, Gval, Eval, Pval)

	// Write the state to the ledger
	err = stub.PutState(A, []byte(strconv.FormatFloat(Aval,'f',2,64))) 
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(B, []byte(strconv.FormatFloat(Bval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(C, []byte(strconv.FormatFloat(Cval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(D, []byte(strconv.FormatFloat(Dval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}
	err = stub.PutState(F, []byte(strconv.FormatFloat(Fval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}
	err = stub.PutState(G, []byte(strconv.FormatFloat(Gval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(E, []byte(strconv.FormatFloat(Eval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(P, []byte(strconv.FormatFloat(Pval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)


}

func (t *SimpleChaincode) Query(stub shim.ChaincodeStubInterface) pb.Response {
		return shim.Error("Unknown supported call")
}

// Transaction makes payment of X units from A to B
func (t *SimpleChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
        fmt.Println("########### example_cc Invoke ###########")
	function, args := stub.GetFunctionAndParameters()
	
	if function != "invoke" {
                return shim.Error("Unknown function call")
	}

	if len(args) < 2 {
		return shim.Error("Incorrect number of arguments. Expecting at least 2")
	}

	if args[0] == "delete" {
		// Deletes an entity from its state
		return t.delete(stub, args)
	}

	if args[0] == "query" {
		// queries an entity state
		return t.query(stub, args)
	}
	if args[0] == "move" {
		// Deletes an entity from its state
		return t.move(stub, args)
	}
	if args[0] == "charge" {
		// Deletes an entity from its state
		return t.charge(stub, args)
	}
	return shim.Error("Unknown action, check the first argument, must be one of 'delete', 'query', or 'move'")
}

func (t *SimpleChaincode) move(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// must be an invoke
	var A, B, C, D, E, P, F, G string    // Entities
	var Aval, Bval, Cval, Dval, Eval, Pval,Fval,Gval float64 // Asset holdings
	var X,Y,Z,W,Q,R,U,V float64          // Transaction value
	var err error


	if len(args) != 17 {
		return shim.Error("Incorrect number of arguments. Expecting 17, function followed by 8 names and 8 value")
	}

	A = args[1]
	B = args[2]
	C = args[3]
	D = args[4]
	F = args[5]
	G = args[6]
	E = args[7]
	P = args[8]
	// Get the state from the ledger
	// TODO: will be nice to have a GetAllState call to ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Avalbytes == nil {
		return shim.Error("Entity not found")
	}
	Aval, _ = strconv.ParseFloat(string(Avalbytes),64)

	Bvalbytes, err := stub.GetState(B)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Bvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Bval, _ = strconv.ParseFloat(string(Bvalbytes),64)

	Cvalbytes, err := stub.GetState(C)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Cvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Cval, _ = strconv.ParseFloat(string(Cvalbytes),64)

	Dvalbytes, err := stub.GetState(D)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Dvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Dval, _ = strconv.ParseFloat(string(Dvalbytes),64)

	Fvalbytes, err := stub.GetState(F)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Fvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Fval, _ = strconv.ParseFloat(string(Fvalbytes),64)	

	Gvalbytes, err := stub.GetState(G)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Gvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Gval, _ = strconv.ParseFloat(string(Gvalbytes),64)

	Evalbytes, err := stub.GetState(E)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Evalbytes == nil {
		return shim.Error("Entity not found")
	}
	Eval, _ = strconv.ParseFloat(string(Evalbytes),64)

	Pvalbytes, err := stub.GetState(P)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Pvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Pval, _ = strconv.ParseFloat(string(Pvalbytes),64)

	// Perform the execution
	X, err = strconv.ParseFloat(args[9],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Y, err = strconv.ParseFloat(args[10],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Z, err = strconv.ParseFloat(args[11],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	W, err = strconv.ParseFloat(args[12],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Q, err = strconv.ParseFloat(args[13],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	R, err = strconv.ParseFloat(args[14],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	U, err = strconv.ParseFloat(args[15],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	V, err = strconv.ParseFloat(args[16],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}

	Aval = Aval + X
	Bval = Bval + Y
	Cval = Cval + Z
	Dval = Dval + W
	Fval = Fval + Q
	Gval = Gval + R
	Eval = U
	Pval = V

	fmt.Printf("Aval = %0.2f, Bval = %0.2f, Cval = %0.2f, Dval = %0.2f, Fval = %0.2f, Gval = %0.2f, Electricity = %0.2f, Price = %0.2f\n", Aval, Bval, Cval, Dval, Fval, Gval, Eval, Pval)

	// Write the state back to the ledger
	err = stub.PutState(A, []byte(strconv.FormatFloat(Aval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(B, []byte(strconv.FormatFloat(Bval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(C, []byte(strconv.FormatFloat(Cval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(D, []byte(strconv.FormatFloat(Dval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(F, []byte(strconv.FormatFloat(Fval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(G, []byte(strconv.FormatFloat(Gval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(E, []byte(strconv.FormatFloat(Eval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(P, []byte(strconv.FormatFloat(Pval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

        return shim.Success(nil);
}

// CHAGRE
func (t *SimpleChaincode) charge(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	// must be an invoke
	var A, B, C, D, E, P, F, G string    // Entities
	var Aval, Bval, Cval, Dval, Eval, Pval, Fval, Gval float64 // Asset holdings
	var X,Y,Z,W,Q,R,U,V float64          // Transaction value
	var err error


	if len(args) != 17 {
		return shim.Error("Incorrect number of arguments. Expecting 17, function followed by 8 names and 8 value")
	}

	A = args[1]
	B = args[2]
	C = args[3]
	D = args[4]
	F = args[5]
	G = args[6]
	E = args[7]
	P = args[8]
	// Get the state from the ledger
	// TODO: will be nice to have a GetAllState call to ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Avalbytes == nil {
		return shim.Error("Entity not found")
	}
	Aval, _ = strconv.ParseFloat(string(Avalbytes),64)

	Bvalbytes, err := stub.GetState(B)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Bvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Bval, _ = strconv.ParseFloat(string(Bvalbytes),64)

	Cvalbytes, err := stub.GetState(C)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Cvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Cval, _ = strconv.ParseFloat(string(Cvalbytes),64)

	Dvalbytes, err := stub.GetState(D)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Dvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Dval, _ = strconv.ParseFloat(string(Dvalbytes),64)

	Fvalbytes, err := stub.GetState(F)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Fvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Fval, _ = strconv.ParseFloat(string(Fvalbytes),64)	

	Gvalbytes, err := stub.GetState(G)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Gvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Gval, _ = strconv.ParseFloat(string(Gvalbytes),64)

	Evalbytes, err := stub.GetState(E)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Evalbytes == nil {
		return shim.Error("Entity not found")
	}
	Eval, _ = strconv.ParseFloat(string(Evalbytes),64)

	Pvalbytes, err := stub.GetState(P)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Pvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Pval, _ = strconv.ParseFloat(string(Pvalbytes),64)

	// Perform the execution
	X, err = strconv.ParseFloat(args[9],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Y, err = strconv.ParseFloat(args[10],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Z, err = strconv.ParseFloat(args[11],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	W, err = strconv.ParseFloat(args[12],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Q, err = strconv.ParseFloat(args[13],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	R, err = strconv.ParseFloat(args[14],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	U, err = strconv.ParseFloat(args[15],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	V, err = strconv.ParseFloat(args[16],64)
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}

	Aval = Aval + X
	Bval = Bval + Y
	Cval = Cval + Z
	Dval = Dval + W
	Fval = Fval + Q
	Gval = Gval + R
	Eval = U
	Pval = V

	fmt.Printf("Aval = %0.2f, Bval = %0.2f, Cval = %0.2f, Dval = %0.2f, Fval = %0.2f, Gval = %0.2f, Electricity = %0.2f, Price = %0.2f\n", Aval, Bval, Cval, Dval, Fval, Gval, Eval, Pval)

	// Write the state back to the ledger
	err = stub.PutState(A, []byte(strconv.FormatFloat(Aval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(B, []byte(strconv.FormatFloat(Bval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(C, []byte(strconv.FormatFloat(Cval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(D, []byte(strconv.FormatFloat(Dval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(F, []byte(strconv.FormatFloat(Fval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(G, []byte(strconv.FormatFloat(Gval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(E, []byte(strconv.FormatFloat(Eval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(P, []byte(strconv.FormatFloat(Pval,'f',2,64)))
	if err != nil {
		return shim.Error(err.Error())
	}

        return shim.Success(nil);
}


// Deletes an entity from state
func (t *SimpleChaincode) delete(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	A := args[1]

	// Delete the key from the state in ledger
	err := stub.DelState(A)
	if err != nil {
		return shim.Error("Failed to delete state")
	}

	return shim.Success(nil)
}

// Query callback representing the query of a chaincode
func (t *SimpleChaincode) query(stub shim.ChaincodeStubInterface, args []string) pb.Response {

	var A string // Entities
	var err error

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to query")
	}

	A = args[1]

	// Get the state from the ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	if Avalbytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	jsonResp := "{\"Name\":\"" + A + "\",\"Amount\":\"" + string(Avalbytes) + "\"}"
	fmt.Printf("Query Response:%s\n", jsonResp)
	return shim.Success(Avalbytes)
}

func main() {
	err := shim.Start(new(SimpleChaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}
