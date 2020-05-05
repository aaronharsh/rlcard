#!/usr/bin/env perl

use strict;
use warnings;

use File::Basename qw(basename);
use List::Util qw(product);


my $show_group = 40;
my $group_size = 10000;

my %rates;
my %layerses;

my %counts_by_rate_layers;
my %sum_loss_by_rate_layers;


sub total_neurons {
    my $layers = shift;
    my @layers = split /x/, $layers;
    return product(@layers);
}


foreach my $file (@ARGV) {
    my $base = basename($file);
    $base =~ s/^output-//;
    $base =~ s/,/x/g;

    my ($rate, $layers) = ($base =~ /^([\d.]*)-(.*)/);

    $rates{$rate} = 1;
    $layerses{$layers} = 1;

    open my $fh, '<', $file or die "Can't read $file: $!";
    while (<$fh>) {
        while (/Agent nfsp0_dqn, step (\d+), rl-loss: ([.\d]*\d)/g) {
            my $step = $1;
            my $loss = $2;

            my $group = int($step / $group_size);
            next unless $group == $show_group;

            $counts_by_rate_layers{$rate}{$layers}++;
            $sum_loss_by_rate_layers{$rate}{$layers} += $loss;
        }
    }
}

my @rates = sort { $a <=> $b } keys %rates;

print join('|', 'layers', @rates), "\n";
foreach my $layers (sort { total_neurons($a) <=> total_neurons($b) } keys %layerses) {
    print $layers;
    foreach my $rate (@rates) {
        my $count = $counts_by_rate_layers{$rate}{$layers};
        my $sum_loss = $sum_loss_by_rate_layers{$rate}{$layers};

        print '|';
        if ($count) {
            print $sum_loss / $count;
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
