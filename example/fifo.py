import os
import asyncio
import argparse

async def write_fifo(fifo_path):
    while True:
        # Data to be written
        data = """TECHNOLOGIES   |   1100 RENE LEVESQUE   |     MONTREAL, PQ||     |TERM #          12000336|RECORD #            0004|HOST INVOICE #   1234567|HOST SEQ #   10012000336|MERCH INVOICE       PU01|------------------------|CARD    ************0256|CREDIT/MASTERCARD      C|3/7/2024 11:14:39 AM    |------------------------|Purchase          $12.00|Tip               $32.00|VOID           |TOTAL             $42.00|------------------------|AUTH#:A27391         B:0|HTS#:     20230107122221|  TRANSACTION  | APPROVED 000 |       THANK YOU|       |Credit                  |AID:  A0000000041010    |TC:   017AA200ACFBD5CC  |TVR:  0440008000        |TSI:  E800|             |     CUSTOMER COPY     |"""

        # Open the FIFO in write mode synchronously
        with open(fifo_path, 'w') as fifo:
            fifo.write(data + '\n')  # Write data synchronously
            print(f"Sent data to FIFO: {fifo_path}")

        await asyncio.sleep(5)  # Small delay between writes

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Write data to a specified FIFO file.")
    parser.add_argument("fifo_path", help="Path to the FIFO file.")
    args = parser.parse_args()

    # Check if the FIFO exists, create it if it doesn't
    if not os.path.exists(args.fifo_path):
        os.mkfifo(args.fifo_path)

    # Run the write task asynchronously
    await write_fifo(args.fifo_path)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
