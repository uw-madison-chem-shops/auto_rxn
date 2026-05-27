import requests


class MksMultigas2030(object):

    def __init__(self):
        self._base_url = "http://localhost/ToolWeb/Cmd"

    def get_prn_path(self) -> str:
        payload = r"""<?xml version="1.0" encoding="utf-8"?>
                      <PollRequest>
                        <V Name="EVID_71"/>
                      </PollRequest>"""
        headers = {"Content-Type": "text/xml; charset=utf-8"}
        requests.request("POST", self._base_url, headers=headers, data=payload)

    def set_prn_path(self, path: str) -> None:
        try:
            payload = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
                          <SetRequest>
                            <V Name=\"EVID_71\">{path}</V>
                          </SetRequest>"""
            headers = {"Content-Type": "text/xml; charset=utf-8"}
            requests.request("POST", self._base_url, headers=headers, data=payload)
        except:
            print("couldn't set prn path!!! oh no")
