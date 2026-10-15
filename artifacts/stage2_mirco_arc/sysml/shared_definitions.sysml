// NOT READY for RTL or high-level model generation
// Snapshot ID: snap-73c872b1307b6adb5eaf843e
// Downstream contract fingerprint: fe7fcb076580a4245cd18758f20d821b4ea5f2e9333b83cbcabaac32735886cf

package ArchitectureShared {

    // Shared definitions for the generated architecture model set.
    connection def ArchitectureConnection {
        attribute signalControl : String;
        attribute trigger : String;
        attribute notes : String;
        attribute sourceRequirementIds : String;
        attribute sourceArtifact : String;
    }
    connection def BlockRelation :> ArchitectureConnection;
    connection def SignalConnection :> ArchitectureConnection;

    port def ArchitecturePort {
        attribute sourceName : String;
        attribute sourceDetails : String;
        attribute sourceTable : String;
        attribute sourcePage : String;
    }

    requirement def SourceRequirement {
        attribute sourceReqId : String;
        attribute sourceArtifact : String;
        attribute sourceContext : String;
    }

}
