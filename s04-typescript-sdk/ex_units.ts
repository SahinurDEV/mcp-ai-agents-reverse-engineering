// ex_units.ts - Exercise 4: convert_units ported to TypeScript, units constrained by a Zod enum.
import { McpServer } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const FACTORS = { km: 1000, m: 1, cm: 0.01, mi: 1609.344, ft: 0.3048 } as const;
const Unit = z.enum(['km', 'm', 'cm', 'mi', 'ft']);

const server = new McpServer({ name: 'units-ts', version: '1.0.0' });

server.registerTool('convert_units', {
  description: 'Convert a length between km, m, cm, mi and ft. Rounded to 4 decimals.',
  inputSchema: z.object({ value: z.number().nonnegative(), from_unit: Unit, to_unit: Unit }),
  outputSchema: z.object({ result: z.number() }),
}, async ({ value, from_unit, to_unit }) => {
  const result = Math.round((value * FACTORS[from_unit] / FACTORS[to_unit]) * 1e4) / 1e4;
  return { content: [{ type: 'text' as const, text: String(result) }], structuredContent: { result } };
});

await server.connect(new StdioServerTransport());
