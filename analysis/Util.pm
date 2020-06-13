package Util;

use strict;
use warnings;

use base 'Exporter';

use List::Util qw(product);

our @EXPORT_OK = qw(
    parse_filename
    read_rl_losses_by_group
    total_neurons_in_layer
);

use constant GROUP_SIZE => 10000;


sub parse_filename {
    my ($filename) = @_;
    $filename =~ /output-(\S+)-([\d.]*)-(.*)/;

    my $activation = $1;
    my $rate = $2;
    my $layers = $3;

    $layers =~ s/,/x/g;

    return {
        activation => $activation,
        rate => $rate,
        layers => $layers,
    };
}


sub total_neurons_in_layer {
    my $layers = shift;
    $layers =~ s/^.*-//;
    my @layers = split /x/, $layers;
    return product(@layers);
}


sub read_rl_losses_by_group {
    my ($file) = @_;

    my %counts_by_group;
    my %sum_loss_by_group;;

    open my $fh, '<', $file or die "Can't read $file: $!";
    while (<$fh>) {
        while (/Agent nfsp0_dqn, step (\d+), rl-loss: ([.\d]*\d)/g) {
            my $step = $1;
            my $loss = $2;

            my $group = int($step / GROUP_SIZE);

            $counts_by_group{$group}++;
            $sum_loss_by_group{$group} += $loss;
        }
    }

    return +{ map {
        $_ => ($sum_loss_by_group{$_} / $counts_by_group{$_})
    } keys %counts_by_group };
}

1;
