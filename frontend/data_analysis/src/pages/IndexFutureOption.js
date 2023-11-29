import React, { useState } from "react";
import DataTable from "./Table";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { Button, LinearProgress, Typography } from "@mui/material";
import "./Future.css";
import dayjs from "dayjs";

function IndexFutureOption() {
  const [date, setDate] = useState(dayjs());
  const [data, setData] = useState();
  const [showTable, setShowTable] = useState(false);
  const [dataNotFound, setDataNotFound] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setDataNotFound(false);
    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/fetch_index_future_and_option_data?date=${date
          .format("DD-MMM-YYYY")
          .toUpperCase()}`
      );
      const data_resp = await response.json();
      // setData(data_resp);
      // console.log(data_resp.response);
      setData(data_resp.response);

      if (data_resp.response[0] == "data_not_found") {
        setData([]);
        setLoading(false);
        setDataNotFound(true);
      } else {
        setShowTable(true);
        setLoading(false);
      }
      // console.log(data);
    } catch (error) {
      console.error(error);
    }
    // console.log();
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div>
        <Typography variant="h3" align="center">
          Index Future And Option Data
        </Typography>
        <div className="datePickWrap">
          <div className="datePick">
            <DatePicker
              label="Select Date"
              value={date}
              onChange={(x) => setDate(x)}
              format="DD-MM-YYYY"
              defaultValue={dayjs()}
            />
            <Button variant="contained" onClick={fetchData}>
              Fetch Data
            </Button>
          </div>
        </div>
        {loading ? <LinearProgress /> : <></>}

        {dataNotFound ? (
          <div className="dataNotFound">
            <Typography variant="h5">Data Not Found</Typography>
          </div>
        ) : (
          <></>
        )}

        {showTable ? <DataTable data={data} /> : <></>}
      </div>
    </LocalizationProvider>
  );
}

export default IndexFutureOption;
