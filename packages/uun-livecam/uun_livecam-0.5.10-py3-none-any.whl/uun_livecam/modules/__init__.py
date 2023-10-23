"""Initialize additional modules."""
from uun_iot import UuAppClient
from uun_livecam.modules.SnapCam import SnapCam


def init(config, uuclient: UuAppClient):
    def uucmd_livecam_snapshot_create(snapshot):
        """
        snapshotCreateDtoIn = {
          cameraCode: "...", // camera code
          tourTs: "...", //tour timestamp
          image: "...", //
          x: 0,
          y: 0,
          zoom: 0
        }
        """
        cam_id, timestamp, image_bin, positions = snapshot
        x = positions["x"]
        y = positions["y"]
        zoom = positions["zoom"]

        uucmd = config["uuApp"]["uuCmdList"]["snapshotCreate"]
        uuclient.multipart(
            uucmd,
            {
                "cameraCode": str(cam_id),
                "tourTs": str(timestamp),
                "x": str(x),
                "y": str(y),
                "zoom": str(zoom),
                "image": ("image.jpeg", image_bin, "image/jpeg"),
            },
        )

        return []  # do not care if failed or succeded, do not save anyway

    gconfig = config["gateway"]

    return [SnapCam(gconfig, uucmd_livecam_snapshot_create)]
