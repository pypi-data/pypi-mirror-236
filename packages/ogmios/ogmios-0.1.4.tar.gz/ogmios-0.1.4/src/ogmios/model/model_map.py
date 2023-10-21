"""This file contains convenient mappings from ogmios.datatypes to ogmios.model.ogmios_model. 
    These mappings combine logical types from the ogmios model that are separated in the schema into
    combined enums that are easier to work with.
"""
from enum import Enum

import ogmios.model.ogmios_model as om


class Types(Enum):
    ebb = om.Type.ebb.value
    bft = om.Type1.bft.value
    praos = om.Type2.praos.value
    stakeDelegation = om.Type3.stakeDelegation.value
    stakeCredentialRegistration = om.Type4.stakeCredentialRegistration.value
    stakeCredentialDeregistration = om.Type5.stakeCredentialDeregistration.value
    stakePoolRegistration = om.Type6.stakePoolRegistration.value
    stakePoolRetirement = om.Type7.stakePoolRetirement.value
    genesisDelegation = om.Type8.genesisDelegation.value
    constitutionalCommitteeHotKeyRegistration = (
        om.Type9.constitutionalCommitteeHotKeyRegistration.value
    )
    constitutionalCommitteeRetirement = om.Type10.constitutionalCommitteeRetirement.value
    delegateRepresentativeRegistration = om.Type11.delegateRepresentativeRegistration.value
    delegateRepresentativeRetirement = om.Type12.delegateRepresentativeRetirement.value
    registered = om.Type13.registered.value
    noConfidence = om.Type14.noConfidence.value
    abstain = om.Type15.abstain.value
    protocolParametersUpdate = om.Type16.protocolParametersUpdate.value
    hardForkInitiation = om.Type17.hardForkInitiation.value
    treasuryTransfer = om.Type18.treasuryTransfer.value
    treasuryWithdrawals = om.Type19.treasuryWithdrawals.value
    constitutionalCommittee = om.Type20.constitutionalCommittee.value
    constitution = om.Type21.constitution.value
    information = om.Type23.information.value
    ipAddress = om.Type24.ipAddress.value
    hostname = om.Type25.hostname.value


class Direction(Enum):
    forward = om.Direction.forward.value
    backward = om.Direction1.backward.value


class Method(Enum):
    findIntersection = om.Method.findIntersection.value
    nextBlock = om.Method4.nextBlock.value
    submitTransaction = om.Method6.submitTransaction.value
    evaluateTransaction = om.Method10.evaluateTransaction.value
    acquireLedgerState = om.Method14.acquireLedgerState.value
    releaseLedgerState = om.Method17.releaseLedgerState.value
    queryLedgerState_epoch = om.Method19.queryLedgerState_epoch.value
    queryLedgerState_eraStart = om.Method19.queryLedgerState_eraStart.value
    queryLedgerState_eraSummaries = om.Method19.queryLedgerState_eraSummaries.value
    queryLedgerState_liveStakeDistribution = (
        om.Method19.queryLedgerState_liveStakeDistribution.value
    )
    queryLedgerState_projectedRewards = om.Method19.queryLedgerState_projectedRewards.value
    queryLedgerState_protocolParameters = om.Method19.queryLedgerState_protocolParameters.value
    queryLedgerState_proposedProtocolParameters = (
        om.Method19.queryLedgerState_proposedProtocolParameters
    ).value
    queryLedgerState_rewardAccountSummaries = (
        om.Method19.queryLedgerState_rewardAccountSummaries.value
    )
    queryLedgerState_rewardsProvenance = om.Method19.queryLedgerState_rewardsProvenance.value
    queryLedgerState_stakePools = om.Method19.queryLedgerState_stakePools.value
    queryLedgerState_utxo = om.Method19.queryLedgerState_utxo.value
    queryLedgerState_tip = om.Method19.queryLedgerState_tip.value
    queryNetwork_blockHeight = om.Method46.queryNetwork_blockHeight.value
    queryNetwork_genesisConfiguration = om.Method48.queryNetwork_genesisConfiguration.value
    queryNetwork_startTime = om.Method50.queryNetwork_startTime.value
    queryNetwork_tip = om.Method52.queryNetwork_tip.value
    acquireMempool = om.Method54.acquireMempool.value
    nextTransaction = om.Method56.nextTransaction.value
    hasTransaction = om.Method57.hasTransaction.value
    sizeOfMempool = om.Method57.sizeOfMempool.value
    releaseMempool = om.Method57.releaseMempool.value


class Era(Enum):
    byron = om.Era3.byron.value
    shelley = om.Era3.shelley.value
    allegra = om.Era3.allegra.value
    mary = om.Era3.mary.value
    alonzo = om.Era3.alonzo.value
    babbage = om.Era3.babbage.value
    conway = om.Era3.conway.value
