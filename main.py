import argparse
from parser import parse_lisp
from geometry import make_cube, apply_transform, make_sphere
from exporter import export_stl

# Minimal evaluator for demo: only supports (cube size)
def eval_expr(expr):
    if isinstance(expr, list):
        if not expr:
            raise ValueError('Empty expression')
        op = expr[0]
        if op == 'cube' and len(expr) == 2:
            return make_cube(float(expr[1]))
        elif op == 'sphere' and len(expr) == 2:
            return make_sphere(float(expr[1]))
        elif op == 'translate' and len(expr) == 5:
            mesh = eval_expr(expr[1])
            x, y, z = float(expr[2]), float(expr[3]), float(expr[4])
            return apply_transform(mesh, (x, y, z))
        else:
            raise ValueError(f'Unknown or invalid expression: {expr}')
    else:
        raise ValueError(f'Invalid atom: {expr}')

def main():
    parser = argparse.ArgumentParser(description='Generate 3D shape from Lisp-like code')
    parser.add_argument('input', help='Input file with Lisp-like code')
    parser.add_argument('-o', '--output', default='out.stl', help='Output STL file')
    args = parser.parse_args()
    with open(args.input) as f:
        code = f.read()
    exprs = parse_lisp(code)
    # Unwrap nested lists if needed
    if not isinstance(exprs, list):
        exprs = [exprs]
    # Flatten if nested (e.g., [[expr1, expr2]])
    if len(exprs) == 1 and isinstance(exprs[0], list):
        exprs = exprs[0]
    for idx, expr in enumerate(exprs):
        mesh = eval_expr(expr)
        out_file = args.output
        if len(exprs) > 1:
            # If multiple expressions, output as out_0.stl, out_1.stl, etc.
            base, ext = args.output.rsplit('.', 1)
            out_file = f"{base}_{idx}.{ext}"
        export_stl(mesh, out_file)
        print(f'Exported STL to {out_file}')

if __name__ == '__main__':
    main()
