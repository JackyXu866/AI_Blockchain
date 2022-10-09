pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract myToken is ERC20{
    constructor() ERC20("My Token", "ETH") {
        _mint(msg.sender, 1000000000000000000000000);
    }
}