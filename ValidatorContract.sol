// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ValidatorContract {
    address public owner;
    mapping(address => bool) public validators;
    address[] public nodes;

    event ValidatorAdded(address indexed validator);
    event NodeAdded(address indexed node);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addValidator(address _validator) public onlyOwner {
        validators[_validator] = true;
        emit ValidatorAdded(_validator);
    }

    function addNode(address _node) public {
        require(validators[msg.sender], "Only validators can add nodes");
        nodes.push(_node);
        emit NodeAdded(_node);
    }

    function getNodes() public view returns (address[] memory) {
        return nodes;
    }
}