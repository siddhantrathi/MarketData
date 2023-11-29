import React, { useState } from "react";
import DataTable from "./Table";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import {
  Button,
  LinearProgress,
  Typography,
  Select,
  FormControl,
  MenuItem,
  InputLabel,
  FormControlLabel,
  Switch,
  FormGroup,
} from "@mui/material";
import "./Strikes.css";
import dayjs from "dayjs";

const TopStrikes = () => {
  const [date, setDate] = useState(dayjs());
  const [data, setData] = useState();
  const [showTable, setShowTable] = useState(false);
  const [dataNotFound, setDataNotFound] = useState(false);
  const [loading, setLoading] = useState(false);
  const [optionType, setOptionType] = useState("");
  const [expiry, setExpiry] = useState(dayjs());
  const [selectExpiry, setSelectExpiry] = useState(false);

  function sequence_data(objArr, seqArr) {
    return objArr.map((obj) => {
      const newObj = {};
      seqArr.forEach((key) => {
        newObj[key] = obj[key];
      });
      return newObj;
    });
  }

  const fetchData = async () => {
    setDataNotFound(false);
    setLoading(true);
    setData([])
    setShowTable(false)
    let response;
    try {
      if (selectExpiry) {
        response = await fetch(
          `http://127.0.0.1:5000/top_5_strikes?date=${date.format(
            "DD-MMM-YYYY"
          )}&option_typ=${optionType}&expiry=${expiry.format("DD-MMM-YYYY")}`
        );
      } else {
        response = await fetch(
          `http://127.0.0.1:5000/top_5_strikes?date=${date.format(
            "DD-MMM-YYYY"
          )}&option_typ=${optionType}`
        );
      }
      const data_resp = await response.json();
      // setData(data_resp);
      // console.log(data_resp.response);

      if (data_resp.response[0] == "data_not_found") {
        setData([]);
        setLoading(false);
        setDataNotFound(true);
        return;
      }
      setShowTable(true);
      setLoading(false);
      setData(
        sequence_data(data_resp.response, [
          "EXPIRY_DT",
          "OPTION_TYP",
          "STRIKE_PR",
          "OPEN_INT",
          "CHG_IN_OI",
          "OPEN",
          "HIGH",
          "LOW",
          "CLOSE",
          "Avg Price",
          "Five Day Avg",
          "Three Day Avg",
        ])
      );

      // console.log(data);
    } catch (error) {
      console.error(error);
    }
    // console.log();
  };

  const handleExpirySwitch = (event) => {
    setSelectExpiry(event.target.checked);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div>
        <Typography variant="h3" align="center">
          Top 5 Strikes
        </Typography>
        <div className="date_pick_wrap">
          <div className="date_pick">
            <DatePicker
              label="Select Date"
              value={date}
              onChange={(x) => setDate(x)}
              format="DD-MM-YYYY"
              defaultValue={dayjs()}
            />
          </div>
          <FormControl className="option_type">
            <InputLabel id="demo-simple-select-label">OPTION TYPE</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={optionType}
              label="OPTION TYPE"
              onChange={(x) => setOptionType(x.target.value)}
              //   onChange={handleChange}
            >
              <MenuItem value={"PE"}>PE</MenuItem>
              <MenuItem value={"CE"}>CE</MenuItem>
            </Select>
          </FormControl>
          <FormGroup>
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Select Expiry"
              checked={selectExpiry}
              onChange={handleExpirySwitch}
            />
          </FormGroup>
          {selectExpiry ? (
            <div className="date_pick">
              <DatePicker
                label="Select Expiry Date"
                value={expiry}
                onChange={(x) => setExpiry(x)}
                format="DD-MM-YYYY"
                defaultValue={dayjs()}
              />
            </div>
          ) : (
            <div className="date_pick">
              <DatePicker
                label="Select Expiry Date"
                value={expiry}
                onChange={(x) => setExpiry(x)}
                format="DD-MM-YYYY"
                disabled
                defaultValue={dayjs()}
              />
            </div>
          )}
          <Button
            variant="contained"
            onClick={fetchData}
            disabled={(optionType == "") || (loading)}
          >
            Fetch Data
          </Button>
        </div>
        {loading ? <LinearProgress /> : <></>}

        {dataNotFound ? (
          <div className="dataNotFound">
            <Typography variant="h5">Data Not Found</Typography>
          </div>
        ) : (
          <></>
        )}

        {showTable ? <DataTable data={data} className="table" /> : <></>}
      </div>
    </LocalizationProvider>
  );
};

export default TopStrikes;
