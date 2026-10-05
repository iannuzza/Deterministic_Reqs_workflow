// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

package STBIO_Shared {

    // Shared definitions for the generated STBIO architecture model set.
    connection def ArchitectureConnection {
        attribute signalControl : String;
        attribute trigger : String;
        attribute notes : String;
        attribute sourceRequirementIds : String;
        attribute sourceArtifact : String;
    }

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
