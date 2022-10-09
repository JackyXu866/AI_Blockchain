pragma solidity >=0.7.0 <0.9.0;

contract xuj14Messenger {
    address private owner;
    uint public changeCounter;
    string public message;


    constructor () {
        owner = msg.sender;
    }

    function updateMessenger(string memory _message) public {
        if(msg.sender == owner){
            message = _message;
            changeCounter++;
        }
    }
}

// SC addr: 0x4A587787b87889a0dB397Fa4a7A8cD94D6D397c9
// https://docs.soliditylang.org/en/v0.8.16/types.html#string-literals-and-types