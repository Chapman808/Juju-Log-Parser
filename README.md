# Juju-Log-Parser

## Summary: 

For this assignment I prioritized customizability over parsing speed. For example, there are a number of times that I could have moved functions into the same loop but chose not to. Instead, I separated each logical operation (i.e. print occurrences of each severity for each charm) into its own code block. Overall, the time complexity should still be O(N).

The only external library I made use of was argparse, for the command line options. 

If I was to improve on this code, I would refactor each operation into its own method for improved readability. I would also move the execution flow under "if __name__ == __main__".  This, of course, would allow the code to be used as a module by other python applications.


## Assumptions:
Where non-conforming lines occur (meaning the line does not fit the log format for juju logs), I assumed that the line belonged to the previous 'proper' entry. For example, the log entry:

machine-8: 01:58:19 DEBUG juju.container.kvm kvm-ok output:

INFO: /dev/kvm exists

KVM acceleration can be used



became one line:

	
machine-8: 01:58:19 DEBUG juju.container.kvm kvm-ok output: INFO: /dev/kvm exists KVM acceleration can be used

## Time spent: 
Overall, I would say I spent about three hours on the code and fifteen minutes on this document. This spanned across a timeframe of about 24 hours.

## Github:
https://github.com/Chapman808/Juju-Log-Parser
