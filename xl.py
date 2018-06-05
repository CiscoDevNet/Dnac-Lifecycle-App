'''

Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

'''

__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"


import xlsxwriter
import time


class xl:

    def __init__(self):
        x = {}

    def date_format(self,epoch_num):
        # convert into secs and make it human readable
        format_date = time.strftime('%Y-%m-%d', time.localtime(epoch_num / 1000))
        return format_date

    def create_xlsxwriter_xl(self, ddata_map):

        workbook = xlsxwriter.Workbook("lifecycle.xlsx")
        dev_sheet = workbook.add_worksheet("Device Info")
        psirt_sheet = workbook.add_worksheet("Security Advisories")
        hweol_sheet = workbook.add_worksheet("Hardware EoL")
        sweox_sheet = workbook.add_worksheet("Software EoL")
        # Formats
        bold = workbook.add_format({'bold': 1})
        big_blue = workbook.add_format()
        big_blue.set_font_size(12)
        big_blue.set_bold()
        #big_blue.set_font_color('blue')
        # Fix the HWEOL column width
        hweol_sheet.set_column("A:A", 25)
        hweol_sheet.set_column("B:B", 30)
        hweol_sheet.set_column("C:C", 25)
        hweol_sheet.set_column("D:D", 20)
        hweol_sheet.set_column("E:E", 15)
        hweol_sheet.set_column("F:F", 15)
        hweol_sheet.set_column("G:G", 15)
        hweol_sheet.set_column("H:H", 15)
        hweol_sheet.set_column("I:I", 20)
        # Fix PSIRT column width
        psirt_sheet.set_column("A:A", 12)
        psirt_sheet.set_column("B:B", 20)
        psirt_sheet.set_column("C:C", 50)
        psirt_sheet.set_column("D:D", 25)
        psirt_sheet.set_column("E:E",10)
        psirt_sheet.set_column("F:F", 45)
        # Fix the SWEOL column width
        sweox_sheet.set_column("A:A", 25)
        sweox_sheet.set_column("B:B", 30)
        sweox_sheet.set_column("C:C", 25)
        sweox_sheet.set_column("D:D", 20)
        sweox_sheet.set_column("E:E", 15)
        sweox_sheet.set_column("F:F", 15)
        sweox_sheet.set_column("G:G", 15)
        sweox_sheet.set_column("H:H", 15)
        sweox_sheet.set_column("I:I", 20)
        # Fix the DEVICES column width
        dev_sheet.set_column("A:A", 25)
        dev_sheet.set_column("B:B", 30)
        dev_sheet.set_column("C:C", 25)
        dev_sheet.set_column("D:D", 20)
        dev_sheet.set_column("E:E", 15)
        dev_sheet.set_column("F:F", 15)
        dev_sheet.set_column("G:G", 15)
        dev_sheet.set_column("H:H", 15)
        # Write HWEOL headers
        hweol_sheet.write('A1', "Hostname", bold)
        hweol_sheet.write('B1', "Type", bold)
        hweol_sheet.write('C1', "PlatformId", bold)
        hweol_sheet.write('D1', "Serial", bold)
        hweol_sheet.write('E1', "Announce Date", bold)
        hweol_sheet.write('F1', "EndofSale Date", bold)
        hweol_sheet.write('G1', "EndofRenewal Date", bold)
        hweol_sheet.write('H1', "EndofSupport Date", bold)
        hweol_sheet.write('I1', "Migration Pid", bold)
        # Write DEVICES headers
        dev_sheet.write('A1', "Hostname", bold)
        dev_sheet.write('B1', "Type", bold)
        dev_sheet.write('C1', "PlatformId", bold)
        dev_sheet.write('D1', "Serial", bold)
        dev_sheet.write('E1', "IP Address", bold)
        dev_sheet.write('F1', "Mac Address", bold)
        dev_sheet.write('G1', "Software Type", bold)
        dev_sheet.write('H1', "Version", bold)
        # Write SWEOL headers
        sweox_sheet.write('A1', "Hostname", bold)
        sweox_sheet.write('B1', "Type", bold)
        sweox_sheet.write('C1', "PlatformId", bold)
        sweox_sheet.write('D1', "Serial", bold)
        sweox_sheet.write('E1', "EndofSale Date", bold)
        sweox_sheet.write('F1', "EndofLife Date", bold)
        sweox_sheet.write('G1', "EndofSupport Date", bold)
        sweox_sheet.write('H1', "URL", bold)
        h_row = 1
        p_row = 1
        s_row = 1
        d_row = 1
        h_col = 0
        p_col = 0
        s_col = 0
        d_col = 0

        # Loop through the data and print it out in XL sheet
        for key, value in ddata_map.items():
            dev_sheet.write(d_row, d_col, ddata_map[key]["hostname"] if ddata_map[key].get("hostname") is not None else "")
            dev_sheet.write(d_row, d_col + 1, ddata_map[key]["type"] if ddata_map[key].get("type") is not None else "")
            dev_sheet.write(d_row, d_col + 2, ddata_map[key]["pid"])
            dev_sheet.write(d_row, d_col + 3,key if key is not None else "")
            dev_sheet.write(d_row, d_col + 4,
                            ddata_map[key]["ip"] if ddata_map[key].get("ip") is not None else "")
            dev_sheet.write(d_row, d_col + 5,
                            ddata_map[key]["mac"] if ddata_map[key].get("mac") is not None else "")
            dev_sheet.write(d_row, d_col + 6,ddata_map[key]["osType"])
            dev_sheet.write(d_row, d_col + 7, ddata_map[key]["swVersion"])

            d_row +=1

            # Print HWEOL data
            if ddata_map[key].get("hweol") != None:
                hweol_sheet.write(h_row, h_col, ddata_map[key]["hostname"] if ddata_map[key].get("hostname") is not None else "")
                hweol_sheet.write(h_row, h_col + 1, ddata_map[key]["type"] if ddata_map[key].get("type") is not None else "")
                hweol_sheet.write(h_row, h_col + 2, ddata_map[key]["pid"])
                hweol_sheet.write(h_row, h_col + 3, key if key is not None else "")

                hweol_sheet.write(h_row, h_col + 4, self.date_format(int(ddata_map[key]["hweol"]["externalAnnounceDate"]))  if ddata_map[key]
                                                                                                        ["hweol"].get("externalAnnounceDate") is not None else "")
                hweol_sheet.write(h_row, h_col + 5,
                              self.date_format(int(ddata_map[key]["hweol"]["hweoxEndOfSaleDate"])) if  ddata_map[key][
                                                                                                          "hweol"].get("hweoxEndOfSaleDate") != None else "")
                hweol_sheet.write(h_row, h_col + 6,
                              self.date_format(int(ddata_map[key]["hweol"]["hweoxSvcRenewalEndDate"])) if ddata_map[key][
                                                                                                          "hweol"].get("hweoxSvcRenewalEndDate") != None else "")
                hweol_sheet.write(h_row, h_col + 7,
                              self.date_format(int(ddata_map[key]["hweol"]["hweoxLastSupportDate"])) if ddata_map[key][
                                                                                                          "hweol"].get("hweoxLastSupportDate") != None else "")
                hweol_sheet.write(h_row, h_col + 8,
                              (ddata_map[key]["hweol"]["migrationPidInfo"][0]["migrationPid"]) if ddata_map[key]["hweol"].get("migrationPidInfo") != None
                                                                                                  and ddata_map[key]["hweol"]["migrationPidInfo"][0].get("migrationPid") != None else "")


                h_row += 1

            # Print SWEOL data
            if ddata_map[key].get("sweol") is not None:
                sweox_sheet.write(s_row, s_col,
                                  ddata_map[key]["hostname"] if ddata_map[key].get("hostname") is not None else "")
                sweox_sheet.write(s_row, s_col + 1,
                                  ddata_map[key]["type"] if ddata_map[key].get("type") is not None else "")
                sweox_sheet.write(s_row, s_col + 2, ddata_map[key]["pid"])
                sweox_sheet.write(s_row, s_col + 3, key)

                sweox_sheet.write(s_row, s_col + 4,
                                  self.date_format(int(ddata_map[key]["sweol"]["sweoxEndOfSaleDate"]))
                                  if ddata_map[key]["sweol"].get("sweoxEndOfSaleDate") != None else "")
                sweox_sheet.write(s_row, s_col + 5,
                                  self.date_format(int(ddata_map[key]["sweol"]["sweoxEndOfLife"]))
                                  if ddata_map[key]["sweol"].get("sweoxEndOfLife") is not None else "")
                sweox_sheet.write(s_row, s_col + 6,
                                  self.date_format(int(ddata_map[key]["sweol"]["sweoxLastSupportDate"]))
                                  if ddata_map[key]["sweol"].get("sweoxLastSupportDate") != None else "")
                sweox_sheet.write(s_row, s_col + 7,
                                  ddata_map[key]["sweol"]["bulletinUrl"] if ddata_map[key]["sweol"].get("bulletinUrl") != None else "")
                s_row += 1


            # Print PSIRT data
            if (ddata_map[key]["psirts"] != None and ddata_map[key]["psirts"] != []):
                psirt_sheet.write(p_row, p_col, "Hostname  :", big_blue)
                psirt_sheet.write(p_row, p_col + 1, ddata_map[key]["hostname"], bold)
                # psirt_sheet.write(p_row, p_col + 2, "Type  :", big_blue)
                # psirt_sheet.write(p_row, p_col + 2, ddata_map[key]["type"],bold)
                psirt_sheet.write(p_row, p_col + 2,
                                  "PId:     " + ddata_map[key]["pid"] + "                      Serial:     " +
                                  key, big_blue)

                psirt_sheet.write(p_row + 2, p_col, "PublishDate", bold)
                psirt_sheet.write(p_row + 2, p_col + 1, "Severity", bold)
                psirt_sheet.write(p_row + 2, p_col + 2, "Description", bold)
                psirt_sheet.write(p_row + 2, p_col + 3, "URL", bold)
                # loop through the PSIRTS
                for psirt in ddata_map[key]["psirts"]:
                    psirt_sheet.write(p_row + 4, p_col, (self.date_format(int(psirt["publishDate"]))))
                    psirt_sheet.write(p_row + 4, p_col + 1, psirt["severityLevelText"] if psirt.get("severityLevelText")
                                                                                          != None else "None")
                    psirt_sheet.write(p_row + 4, p_col + 2, psirt["headlineName"] if psirt.get("headlineName")
                                                                                      != None else "None")
                    psirt_sheet.write(p_row + 4, p_col + 3, psirt["psirtUrlText"] if psirt.get("psirtUrlText")
                                      != None else "None")
                    p_row += 1
                p_row += 6  # 2 blank rows b4 & after psirt headers & 2 headers
            else:
                psirt_sheet.write (p_row, p_col + 1, "No PSIRTs found for  --  " + ddata_map[key]["hostname"] +
                                   "      PId -- "+
                                   ddata_map[key]["pid"] +  "       OS version -- " + ddata_map[key]["swVersion"])
                p_row += 2  # 2 blank rows b4 & after psirt headers & 2 headers

