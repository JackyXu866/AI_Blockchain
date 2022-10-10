pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: MIT

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract myToken is ERC20{
    constructor() ERC20("Ethereum", "ETH") {
        _mint(msg.sender, 1000000000000000000000000);
    }
}

// 0x26C3251dD6ffA57aC87BEF41c40d6ac296608a06