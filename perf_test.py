from bartiq import Routine, compile_routine
from bartiq.symbolics import sympy_backend

N_CHILDREN = 1000


def test_compilation_works_as_expected_in_presence_of_large_number_of_children(
    backend, transitive_resources, expected_t_count, expected_foo
):
    # This test does not check correctness, but rather serves as litmus paper detecting performance
    # regression. See https://github.com/PsiQ/bartiq/issues/181

    qref_def = {
        "version": "v1",
        "program": {
            "name": "root",
            "type": "root",
            "input_params": ["n"],
            "children": [
                {
                    "name": f"child_{i}",
                    "resources": [
                        {"type": "additive", "name": "t_count", "value": "n"},
                        {"type": "multiplicative", "name": "foo", "value": "n"},
                    ],
                }
                for i in range(N_CHILDREN)
            ],
        },
    }

    routine = Routine.from_qref(qref_def, backend)
    compilation_result = compile_routine(routine, backend=backend).routine


test_compilation_works_as_expected_in_presence_of_large_number_of_children(
    sympy_backend,
    False,
    f"{N_CHILDREN}*n",
    f"n ^ {N_CHILDREN}",
    # test for trasntive_rources=True below be sure to add it back to the compile_routine params on line 32
    # sympy_backend, True, " + ".join(sorted(f"child_{x}.t_count" for x in range(N_CHILDREN))), "*".join(sorted(f"child_{x}.foo" for x in range(N_CHILDREN))),
)
