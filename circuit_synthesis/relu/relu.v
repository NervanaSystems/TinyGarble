`timescale 1ns / 1ps

module relu
#(
	parameter N=32, // Bit-width of inputs to sum
	parameter M=1  // Number of inputs to process
)
(
	clk,
	rst,
	g_input,
	e_input, // learns the output
	o
);

	input clk, rst;
	input[2*M*N-1:0] g_input; // List of M 2 N-bit numbers; ([r_1, r_2], [r_1, r_2], ...)
	input[M*N-1:0] e_input;   // List of M N-bit numbers [x-r_1]
	output [M*N-1:0] o;       // Relu(x) - r_2

	wire [N-1:0] x; // Holds reconstructed secret
	wire [M*N-1:0] r1;
	wire [M*N-1:0] r2;

	generate
	if(M>1)
	begin
		assign o = r1;
	end
	else
	begin
		assign r1 = g_input[2*N-1:N];
		assign r2 = g_input[N-1:0];

		wire overflow;

		// Reconstruct x (mod 2**N)
		ADD #( .N(N) ) OP1
		(
			.A(r1),
			.B(e_input),
			.CI(1'b0), // No carry in
			.S(x),     // Sum is stored in output
			.CO(overflow) // Carry-out put into MSB of x, since we need additional 2^31.
		);

		wire [N-1:0] relu_x;

		// overflow => x > 0
		always@* begin
			if (overflow) begin
				relu_x = x;
			end
			else begin
				relu_x = 0;
			end
		end
		// relu_x is 2^31 smaller than the desired output.
		// However, we mask with r2, so the 2^31 is restored.
		// Mask with r2; store result in o
		ADD #( .N(N) ) OP3
		(
			.A(relu_x),
			.B(r2),
			.S(o),
			.CO()
		);
	end
	endgenerate




endmodule

