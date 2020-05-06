#!/usr/bin/env perl

use strict;
use warnings;

use FindBin;
use lib $FindBin::Bin;

use Util qw(
    parse_filename
    read_rl_losses_by_group
    total_neurons_in_layer
);


my $show_group = 40;


my %rows;
my %columns;
my %rl_loss_by_row_column;


sub activation {
    my ($row) = @_;
    return $row =~ s/-.*//r;
}


foreach my $file (@ARGV) {
    my $file_info = parse_filename($file);

    my $row = "$file_info->{activation}-$file_info->{layers}";
    my $column = $file_info->{rate};

    $rows{$row} = 1;
    $columns{$column} = 1;

    my $rl_loss_by_group = read_rl_losses_by_group($file);
    $rl_loss_by_row_column{$row}{$column} = $rl_loss_by_group->{$show_group};
}

my @columns = sort { $a <=> $b } keys %columns;

print join('|', 'layers', @columns), "\n";
foreach my $row (sort { activation($a) cmp activation($b) || total_neurons_in_layer($a) <=> total_neurons_in_layer($b) } keys %rows) {
    print $row;
    foreach my $column (@columns) {
        my $loss = $rl_loss_by_row_column{$row}{$column};

        print '|';
        if (defined $loss) {
            print $loss;
        }
    }
    print "\n";
}

__END__
----------------------------------------
  timestamp    |  2020-05-04 05:56:12
  timestep     |  2
  reward       |  -0.1662
----------------------------------------
Evaluation of ['A-S', '5-C', '5-H', '5-D']: choose A-S, probs = [('A-S', 0.30766039271671675), ('5-C', 0.23585892684143314), ('5-H', 0.24083382427009203), ('5-D', 0.21564685617175805)]
Evaluation of ['A-C', 'A-H', 'A-D', 'J-D']: choose A-D, probs = [('A-C', 0.1417882707195071), ('A-H', 0.21444494237249528), ('A-D', 0.3497132287423578), ('J-D', 0.2940535581656399)]
Evaluation of ['2-C', '3-H', '6-D', '7-D']: choose 2-C, probs = [('2-C', 0.26411833987298045), ('3-H', 0.24010953906571764), ('6-D', 0.25125885738838794), ('7-D', 0.24451326367291398)]
INFO - Agent nfsp0_dqn, step 1000, rl-loss: 0.6703484654426575
