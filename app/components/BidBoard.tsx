'use client'

import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from '@mui/material';
import axios from 'axios';

// Updated Bid type to match the backend response
type Bid = {
  id: string;
  sendername: string; // Assuming camelCase conversion
  streetaddress: string;
  status: string;
  assignedto: string;
  bidamount: number;
};

// Define a type for pagination metadata
type PaginationMeta = {
  page: number;
  pages: number;
  total_count: number;
  per_page: number;
}

const BidsTable = () => {
  console.log("BidsTable component is mounting");
  const [bids, setBids] = useState<Bid[]>([]);
  const [editBidId, setEditBidId] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [paginationMeta, setPaginationMeta] = useState<PaginationMeta | null>(null);

  // Fetch bids from your API with pagination
  useEffect(() => {
    console.log('Fetching bids...');
    axios.get(`http://localhost:3001/bids?page=${currentPage}&per_page=30`)
      .then((res) => {
        console.log('Response data:', res.data);
        setBids(res.data.bids);
        setPaginationMeta(res.data.meta);
      })
      .catch((error) => {
        console.error('Fetch error:', error.message);
      });
  }, [currentPage]);

  // Log the bids to the console to verify they are being fetched
  console.log(bids);

  // Pagination controls
  const goToNextPage = () => {
    setCurrentPage(currentPage + 1);
  };

  const goToPrevPage = () => {
    setCurrentPage(currentPage - 1);
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Sender Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Assigned To</TableCell>
              <TableCell>Bid Amount</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bids.map((bid) => (
              <TableRow key={bid.id}>
                <TableCell>{bid.sendername}</TableCell>
                <TableCell>{bid.status}</TableCell>
                <TableCell>{bid.assignedto}</TableCell>
                <TableCell>${bid.bidamount}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={goToPrevPage} disabled={!paginationMeta?.page || paginationMeta?.page === 1}>Previous</Button>
        <span>Page {paginationMeta?.page} of {paginationMeta?.pages}</span>
        <Button onClick={goToNextPage} disabled={!paginationMeta?.pages}>Next</Button>
      </div>
    </>
  );
};

export default BidsTable;

