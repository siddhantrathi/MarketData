import React from "react";
import { Typography, Button } from "@mui/material";
import "./Home.css";

const Home = () => {
  return (
    <div>
      <Typography variant="h2" align="center">
        Welcome To Home
      </Typography>
      <div className="LinksForDataContainer">
        <Typography variant="h4" align="center">
          Links For Data:
        </Typography>
        <div className="ButtonsContainer">
          <Button variant="contained" href="/fao_participation_oi">
            Future And Option Participation Open Interest
          </Button>
          <Button variant="contained" href="/index_future_option">
            Index Future And Option Data
          </Button>
          <Button variant="contained" href="/top_strikes">
            Top 5 Strikes
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Home;
