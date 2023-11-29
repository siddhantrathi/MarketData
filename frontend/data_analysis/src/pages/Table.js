import React from "react";
import { styled } from "@mui/material/styles";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

const DataTableContainer = styled(TableContainer)(({ theme }) => ({
  maxWidth: "100%",
  margin: "auto",
  marginBottom: theme.spacing(3),
}));

const DataTableTable = styled(Table)({
  minWidth: 650,
});

const DataTableDarkRow = styled(TableRow)(({ theme }) => ({
  backgroundColor: theme.palette.grey[100],
}));

const DataTableLightRow = styled(TableRow)(({ theme }) => ({
  backgroundColor: theme.palette.common.white,
}));


function DataTable({ data }) {
  const columns = Object.keys(data[0]);
  const dateIndex = columns.indexOf("Date");

  if (dateIndex !== -1) {
    // Move the "Date" column to the front of the array
    columns.splice(dateIndex, 1);
    columns.unshift("Date");
  }

  return (
    <DataTableContainer component={Paper}>
      <DataTableTable>
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell key={column}>{column}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <React.Fragment key={index}>
              {index % 2 === 0 ? (
                <DataTableDarkRow>
                  {columns.map((column) => (
                    <TableCell key={column}>{row[column]}</TableCell>
                  ))}
                </DataTableDarkRow>
              ) : (
                <DataTableLightRow>
                  {columns.map((column) => (
                    <TableCell key={column}>{row[column]}</TableCell>
                  ))}
                </DataTableLightRow>
              )}
            </React.Fragment>
          ))}
        </TableBody>
      </DataTableTable>
    </DataTableContainer>
  );
}

export default DataTable;
