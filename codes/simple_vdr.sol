// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0;

contract simpleVDR {
    mapping(string => string) _mapVDR;

    function register(string memory _did, string memory _document) public {
        _mapVDR[_did] = _document;
    }

    function resolve(string memory _did) public view returns (string memory) {
        return _mapVDR[_did];
    }
}