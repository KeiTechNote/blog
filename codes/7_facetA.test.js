/* eslint-disable prefer-const */
/* global contract artifacts web3 before it assert */

const Diamond = artifacts.require('Diamond')
const DiamondCutFacet = artifacts.require('DiamondCutFacet')
const DiamondLoupeFacet = artifacts.require('DiamondLoupeFacet')
const OwnershipFacet = artifacts.require('OwnershipFacet')
const FacetA = artifacts.require('FacetA')
const FacetCutAction = {
    Add: 0,
    Replace: 1,
    Remove: 2
}

const zeroAddress = '0x0000000000000000000000000000000000000000';

function getSelectors (contract) {
    const selectors = contract.abi.reduce((acc, val) => {
        if (val.type === 'function') {
        acc.push(val.signature)
        return acc
        } else {
        return acc
        }
    }, [])
    return selectors
}

contract('FacetA Test', async (accounts) => {

    it('should add FacetA functions', async () => {
        let facetA = await FacetA.deployed();
        let selectors = getSelectors(facetA);
        let addresses = [];
        addresses.push(facetA.address);
        let diamond  = await Diamond.deployed();
        let diamondCutFacet = await DiamondCutFacet.at(diamond.address);
        await diamondCutFacet.diamondCut([[facetA.address, FacetCutAction.Add, selectors]], zeroAddress, '0x');

        let diamondLoupeFacet = await DiamondLoupeFacet.at(diamond.address);
        result = await diamondLoupeFacet.facetFunctionSelectors(addresses[0]);
        assert.sameMembers(result, selectors)
    })

    it('should test function call', async () => {
        let diamond  = await Diamond.deployed();
        let facetAViaDiamond = await FacetA.at(diamond.address);
        const dataToStore = '0xabcdef';
        await facetAViaDiamond.setDataA(dataToStore);
        let dataA = await facetAViaDiamond.getDataA();
        assert.equal(dataA,web3.eth.abi.encodeParameter('bytes32', dataToStore));
    })

})