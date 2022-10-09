pragma solidity >=0.7.0 <0.9.0;

contract xuj14Wallet {
    address public owner;
    bool public limit;
    uint public limitAmount;
    address[5] private guardian;
    mapping(address => bool) private guardianVote;
    bool public hasGuardian;
    address public toChange;


    constructor () {
        owner = msg.sender;
        limit = false;
    }

    receive() external payable {}

    function pay(uint _amount, address _sendto) external payable {
        require(msg.sender == owner, "You are not the owner of the wallet");
        require(address(this).balance >= _amount, "Not enough money in the wallet");
        if(limit == true){
            require(limitAmount>=_amount, "Exceed the limit of spending");
            // lower the limit because already spent (not sure if needed)
            limitAmount -= _amount;
        }
        payable(_sendto).call{value: _amount}("");
    }

    function setLimit(uint _amount) public {
        limit = true;
        // didnt check if limit amount is larger than account balance
        // because it is going to be checked when transferring
        limitAmount = _amount;
    }

    function setGuardian(address[5] memory _guardian) public {
        require(msg.sender == owner, "You are not the owner of the wallet");
        // check if all 5 guardians are filled.
        for(uint i=0; i<5; i++){
            require(_guardian[i]!=address(0), "Guardian address invalid");
        }
        // have to loop twice to avoid invalid situation
        for(uint i=0; i<5; i++){
            guardianVote[_guardian[i]] = false;
        }
        guardian = _guardian;
        hasGuardian = true;
    }

    // anyone could start change address procedure
    // which require 3 of 5 guardians to check in
    function changeAddress() public {
        require(hasGuardian == true, "Guardians not set");
        for(uint i=0; i<5; i++){
            guardianVote[guardian[i]] = false;
        }
        toChange = msg.sender;
    }

    function verify() public {
        require(toChange != address(0), "Invalid address to change");
        uint count = 0;
        for(uint i=0; i<5; i++){
            if(guardian[i] == msg.sender) guardianVote[guardian[i]] = true;
            if(guardianVote[guardian[i]] == true) count++;
        }
        if(count>=3) owner = toChange;
    }
}

// https://docs.soliditylang.org/en/latest/cheatsheet.html#function-visibility-specifiers
// https://docs.soliditylang.org/en/latest/types.html
// https://blockchain-academy.hs-mittweida.de/courses/solidity-coding-beginners-to-intermediate/lessons/solidity-2-sending-ether-receiving-ether-emitting-events/topic/sending-ether-send-vs-transfer-vs-call/