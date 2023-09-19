const FacetA = artifacts.require('Test2Facet')

module.exports = function (deployer, network, accounts) {
    deployer.deploy(FacetA)
}