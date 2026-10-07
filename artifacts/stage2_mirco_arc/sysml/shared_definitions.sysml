// Snapshot ID: snap-b2e8101b00dc6909feaed885
// Downstream contract fingerprint: 8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372

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
