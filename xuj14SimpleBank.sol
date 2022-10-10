pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: MIT

contract xuj14SimpleBank {
    mapping(address => uint) public balances;

    function deposit () public payable {
        balances[msg.sender] += msg.value;
    }

    function getContractBalance () public view returns(uint) {
        return balances[msg.sender];
     }

    function withdraw (uint _amount) public payable{
        require(balances[msg.sender]>=_amount, "Not enough balance to withdraw.");
        balances[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
    }

    function withdrawAll () public payable{
        uint amount = balances[msg.sender];
        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}

// SC addr: 0x2c62B9Aae58956F08905F5dE1370ADF3A4fCBc2f
// https://www.tutorialspoint.com/solidity/solidity_mappings.htm
// https://www.tutorialspoint.com/solidity/solidity_functions.htm#:~:text=The%20return%20Statement,function%20to%20return%20a%20string.
