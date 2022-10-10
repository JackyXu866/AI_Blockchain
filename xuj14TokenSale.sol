pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: MIT

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract xuj14TokenSale {
    IERC20 public token;  
    address public owner;
    uint public ratio;

    constructor (address _tokenAddress, uint _ratio) {
        owner = msg.sender;
        token = IERC20(_tokenAddress);
        ratio = _ratio;
    }

    // supply the sale with amount of tokens
    // although it is not needed, I could just use metamask to send
    // token to this address.
    function supply(uint _amount) public {
        require(msg.sender==owner, "You must be the owner to supply tokens.");
        require(token.balanceOf(msg.sender)>=_amount, "Not enough token for supplying.");
        uint allowance = token.allowance(msg.sender, address(this));
        require(allowance >= _amount, "Check the token allowance");
        token.transferFrom(msg.sender, address(this), _amount);
    }

    function buy() external payable {
        require(token.balanceOf(address(this))>=msg.value*ratio, "Not enough token to supply");

        token.transfer(msg.sender,  msg.value*ratio);
    }

    function balance() public view returns(uint){
        return token.balanceOf(address(this));
    }
}

// 0x1727eEdeF71e94DD1daCfa5E5C5cDac19023028b
// https://stackoverflow.com/questions/71808619/erc20-insufficient-
// https://docs.openzeppelin.com/contracts/4.x/api/token/erc20#ERC20