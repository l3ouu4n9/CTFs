// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
contract AccessmyContract{
    string public flag = "Password";
    function verify(string memory _flag) public view returns (bool){
        require(keccak256(abi.encode(flag)) == keccak256(abi.encode(_flag)));
        return true;
    }
}