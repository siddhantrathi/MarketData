import React, { useState } from "react";
import dayjs from "dayjs";
import {
  Typography,
  Button,
  Table,
  TableBody,
  TableContainer,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
} from "@mui/material";
import "./Fao.css";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

const FaoParticipationOI = () => {
  const [date, setDate] = useState(dayjs());
  const [faoData, setFaoData] = useState();
  const [showTable, setShowTable] = useState("blank");
  const [loading, setLoading] = useState(false);
  const [processedFaoData, setProcessedFaoData] = useState();

  async function getData() {
    setLoading(true);
    setShowTable("blank");
    setFaoData([]);
    let day = ("0" + date.date().toString()).slice(-2);
    let month = ("0" + (date.month() + 1).toString()).slice(-2);
    let year = date.year().toString();

    const fullDate = day + month + year;
    console.log(fullDate);

    await fetch(
      `http://localhost:5000/fetch_fao_participation_oi?date=${fullDate}`
    )
      .then((res) => res.json())
      .then(async (data) => {
        setFaoData(data.response[0]);
        if (data.response[1] === "data not found") {
          setShowTable("no");
        } else if (data.response[1] === "success") {
          await fetch(
            `http://localhost:5000/fetch_processed_fao_participation_oi?date=${fullDate}`
          )
            .then((resp) => resp.json())
            .then((p_data) => {
              setProcessedFaoData(p_data.response[0]);
            })
            .catch((err) => {
              console.log(err.message);
            });
          setShowTable("yes");
        } else {
          alert("Error");
        }
        setLoading(false);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div>
        <div className="heading">
          <Typography variant="h3" gutterBottom>
            Future And Option Participation Open Interest
          </Typography>
        </div>
        <div className="datePickWrap">
          <div className="datePick">
            <DatePicker
              label="Select Date"
              value={date}
              onChange={(x) => setDate(x)}
              format="DD-MM-YYYY"
              defaultValue={dayjs()}
            />
            <Button variant="contained" onClick={getData}>
              Get Data
            </Button>
          </div>
        </div>
        {loading ? <LinearProgress className="Loader" /> : <></>}
        {/* <LinearProgress className="Loader" /> */}
        <div className="tableContainer">
          {showTable === "yes" ? (
            <div>
              <Typography variant="h5" align="center" className="rawDataHeader">
                Raw Data
              </Typography>
              <RawDataTable faoData={faoData} date={date} />
              <Typography
                variant="h5"
                align="center"
                className="processedDataHeader"
              >
                Processed Data
              </Typography>
              <ProcessedFaoDataTable faoData={processedFaoData} date={date} />
            </div>
          ) : (
            <div>
              {showTable === "no" ? (
                <Typography
                  variant="h5"
                  align="center"
                  className="noDataHeader"
                >
                  Data Not Found
                </Typography>
              ) : (
                <></>
              )}
            </div>
          )}
        </div>
      </div>
    </LocalizationProvider>
  );
};

const RawDataTable = (props) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Client Type</TableCell>
            <TableCell align="right">Future Index Long</TableCell>
            <TableCell align="right">Future Index Short</TableCell>
            <TableCell align="right">Future Stock Long</TableCell>
            <TableCell align="right">Future Stock Short</TableCell>
            <TableCell align="right">Option Index Call Long</TableCell>
            <TableCell align="right">Option Index Call Short</TableCell>
            <TableCell align="right">Option Index Put Long</TableCell>
            <TableCell align="right">Option Index Put Short</TableCell>
            <TableCell align="right">Option Stock Call Long</TableCell>
            <TableCell align="right">Option Stock Call Short</TableCell>
            <TableCell align="right">Option Stock Put Long</TableCell>
            <TableCell align="right">Option Stock Put Short</TableCell>
            <TableCell align="right">Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.faoData.map((row) => (
            <TableRow
              key={row["Client Type"]}
              sx={{
                "&:last-child td, &:last-child th": { border: 0 },
              }}
            >
              <TableCell component="th" scope="row">
                {row["Client Type"]}
              </TableCell>
              <TableCell align="right">{row["Future Index Long"]}</TableCell>
              <TableCell align="right">{row["Future Index Short"]}</TableCell>
              <TableCell align="right">{row["Future Stock Long"]}</TableCell>
              <TableCell align="right">{row["Future Stock Short"]}</TableCell>
              <TableCell align="right">
                {row["Option Index Call Long"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Index Call Short"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Index Put Long"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Index Put Short"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Stock Call Long"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Stock Call Short"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Stock Put Long"]}
              </TableCell>
              <TableCell align="right">
                {row["Option Stock Put Short"]}
              </TableCell>
              <TableCell align="right">
                {`${props.date.date()}/${
                  props.date.month() + 1
                }/${props.date.year()}`}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

function ProcessedFaoDataTable(props) {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Client Type</TableCell>
            <TableCell align="right">Future Position</TableCell>
            <TableCell align="right">Future Long OI</TableCell>
            <TableCell align="right">Future Short OI</TableCell>
            <TableCell align="right">Call Long OI</TableCell>
            <TableCell align="right">Call Short OI</TableCell>
            <TableCell align="right">Put Long OI</TableCell>
            <TableCell align="right">Put Short OI</TableCell>
            <TableCell align="right">Future Long Short Ratio</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.faoData.map((row) => (
            <TableRow
              key={row["Client Type"]}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row["Client Type"]}
              </TableCell>
              <TableCell align="right">{row["Future Position"]}</TableCell>
              <TableCell align="right">{row["Future Long OI"]}</TableCell>
              <TableCell align="right">{row["Future Short OI"]}</TableCell>
              <TableCell align="right">{row["Call Long OI"]}</TableCell>
              <TableCell align="right">{row["Call Short OI"]}</TableCell>
              <TableCell align="right">{row["Put Long OI"]}</TableCell>
              <TableCell align="right">{row["Put Short OI"]}</TableCell>
              <TableCell align="right">
                {row["Future Long Short Ratio"]}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default FaoParticipationOI;
