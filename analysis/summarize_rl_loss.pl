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


my $group_size = 10000;

my %columns;
my %groups;

my %loss_by_column_group;


foreach my $file (@ARGV) {
    my $file_info = parse_filename($file);

    my $column = "$file_info->{activation}-$file_info->{rate}-$file_info->{layers}";

    $columns{$column} = 1;

    my $rl_losses_by_group = read_rl_losses_by_group($file);
    while (my ($group, $loss) = each %$rl_losses_by_group) {
        $groups{$group} = 1;
        $loss_by_column_group{$column}{$group} = $loss;
    }
}

my @columns = sort keys %columns;

print join('|', 'group', @columns), "\n";
foreach my $group (sort { $a <=> $b } keys %groups) {
    print $group;
    foreach my $column (@columns) {
        my $loss = $loss_by_column_group{$column}{$group};

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
